"""collection_client.py
============
The extended client module for collection campaigns.
"""

import os
import datetime
from random import random
import time
import uuid
import json
from uuid import uuid4
from io import IOBase
from tempfile import NamedTemporaryFile
from tqdm import tqdm
from google.resumable_media.requests import ChunkedDownload
from google.resumable_media.common import InvalidResponse, DataCorruption
from typing import Any, Callable, Optional, Union, List, Dict, Tuple

from requests.adapters import prepend_scheme_if_needed

from .util import (
    requests_retry,
    raise_resp_exception_error,
    _is_one_gb_available,
    _upload_local_files,
    create_temp_directory,
    mark_temp_directory_complete,
    MAX_CHUNK_SIZE,
    MAX_FRAMES_PER_BATCH,
)
from .client import Client
from .dataset import LabeledDataset, LabeledFrame
from .inference import Inferences, InferencesFrame
from .sampling_agent import RandomSamplingAgent

from .embedding_distance_sampling import EmbeddingDistanceSamplingAgent


class CollectionClient(Client):
    """Client class that interacts with the Aquarium REST API.
    Also handles extra work around collecting samples for collection campigns

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    def __init__(self, *args, **kwargs) -> "CollectionClient":
        super().__init__(*args, **kwargs)
        self.active_coll_camp_summaries = []

        self.sampling_agent = EmbeddingDistanceSamplingAgent
        self.camp_id_to_sample_agent = {}

        self.frame_batch_uuid_to_temp_file_path = {}
        self.frame_batch_uuid_to_camp_id_to_probability_score_info = {}

        # A mapping of campaign ID to the list of GCS URLs (one URL per batch of frames)
        self.camp_id_to_gcs_frame_urls = {}

        self.temp_file_path = create_temp_directory()

    def _save_content_to_temp(
        self, file_name_prefix: str, writefunc: Callable, mode: str = "w"
    ) -> Optional[str]:
        """saves whatever the write function wants to a temp file and returns the file path

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=self.temp_file_path
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def write_to_file(self, frames: List[Dict[str, any]], filelike: IOBase) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in frames:
            filelike.write(json.dumps(frame) + "\n")

    def download_to_file(self, signed_url: str, filelike: IOBase) -> None:
        xml_api_headers = {
            "content-type": "application/octet-stream",
        }
        download = ChunkedDownload(signed_url, MAX_CHUNK_SIZE, filelike)
        while not download.finished:
            try:
                download.consume_next_chunk(requests_retry)
            except (InvalidResponse, DataCorruption, ConnectionError):
                if download.invalid:
                    continue
                continue

    def _read_rows_from_disk(self, file_path: str) -> List[Dict[str, Any]]:
        """reads temp files from disk and loads the dicts in them into memory

        Args:
            file_path (str): file path to read from

        Returns:
            List[Dict[str, Any]]: List of LabeledFrames in a dict structure
        """
        with open(file_path, "r") as frame_file:
            return [json.loads(line.strip()) for line in frame_file.readlines()]

    def _get_all_campaigns(
        self, target_project_names: List[str] = []
    ) -> List[Dict[str, Any]]:
        """Gets all collection campaign summaries (filtered to the target_project_names if provided)

        Args:
            target_project_names (Optional[List[str]], optional): List of project names whose collection campaigns should be sampled for

        Returns:
            List[Dict[str, Any]]: List of dicts containing collection campaign summaries
        """
        params = (
            {"target_project_names": target_project_names}
            if target_project_names
            else {}
        )

        r = requests_retry.get(
            self.api_endpoint + "/collection_campaigns/summaries",
            headers=self._get_creds_headers(),
            params=params,
        )

        raise_resp_exception_error(r)
        return r.json()

    def _upload_collection_frames_to_gcs(
        self,
        frame_batch_uuid: str,
        campaign_id: str,
        collection_frames: Dict[str, Any],
    ) -> List[str]:
        """takes frames for collection and posts it to the API in batches

        Args:
            frame_batch_uuid (str): The local frame batch these frames were sampled from
            campaign_id (str): The collection campaign id
            collection_frames (Dict[str, Any]): Dict structure containing all the collected frames for a campaign to post

        Returns:
            List[str]: List of GCS URLs corresponding to the uploaded frame batches
        """

        def batches(lst, size):
            for i in range(0, len(lst), size):
                yield lst[i : i + size]

        def save_batch(frames):
            current_time = datetime.datetime.now()
            # Write frames to local temp file
            temp_frame_prefix = "al_{}_sampled_frames_{}_".format(
                current_time.strftime("%Y%m%d_%H%M%S_%f"), frame_batch_uuid
            )
            temp_frame_path = self._save_content_to_temp(
                temp_frame_prefix,
                lambda x: self.write_to_file([frame for frame in frames], x),
            )
            return temp_frame_path

        # Get upload / download URLs
        download_urls = []
        get_upload_path = (
            f"{self.api_endpoint}/collection_campaigns/{campaign_id}/get_upload_url"
        )

        frame_batch_filepaths = [
            save_batch(batched_frames)
            for batched_frames in batches(collection_frames, MAX_FRAMES_PER_BATCH)
        ]

        download_urls = _upload_local_files(
            frame_batch_filepaths,
            get_upload_path,
            self._get_creds_headers(),
            frame_batch_uuid,
            ".jsonl",
            delete_after_upload=True,
        )

        return download_urls

    def _post_collection_frames(self, payload: Dict[str, Any]) -> None:
        """takes a payload and posts it to the API

        Args:
            payload (Dict[str, Any]): Dict structure containing the payload for a campaign to post
        """
        print(
            f"Saving collection frames for campaign ID {payload['collection_campaign_id']}..."
        )

        r = requests_retry.post(
            self.api_endpoint + "/projects/blah/collection_frames",
            headers=self._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)
        return r.json()

    def _is_postprocessing_complete(self, campaign_summary: Dict[str, Any]) -> bool:
        return campaign_summary.get("pca_signed_url") and campaign_summary.get(
            "microcluster_info_signed_url"
        )

    def sync_state(self, target_project_names: List[str] = []) -> None:
        """Downloads all collection campaigns and preps sampler with sample frames

        Args:
            target_project_names (Optional[List[str]], optional): List of project names whose collection campaigns should be sampled for
        """
        print("Starting Sync")
        all_coll_camps = self._get_all_campaigns(target_project_names)

        # Skip over collection campaigns that still need to be post-processed
        processing_coll_camps_issue_uuids = [
            c.get("issue_uuid")
            for c in all_coll_camps
            if c["active"] and not self._is_postprocessing_complete(c)
        ]
        if len(processing_coll_camps_issue_uuids) > 0:
            print(
                f"{len(processing_coll_camps_issue_uuids)} collection campaigns still awaiting postprocessing."
            )
            for issue_uuid in processing_coll_camps_issue_uuids:
                print(f" - issue uuid: {issue_uuid}")

        self.active_coll_camp_summaries = [
            c
            for c in all_coll_camps
            if c["active"] and self._is_postprocessing_complete(c)
        ]
        print(
            f"Found {len(self.active_coll_camp_summaries)} Active Collection Campaigns"
        )

        # Initialize a sampling agent per active, postprocessed campaign
        self.camp_id_to_sample_agent = {
            c["id"]: self.sampling_agent() for c in self.active_coll_camp_summaries
        }

        print(f"Downloading assets for each Collection Campaign")
        for campaign in self.active_coll_camp_summaries:
            # download each of the preprocessed files for the example dataset locally
            signed_urls = {
                "pca_signed_url": campaign.get("pca_signed_url"),
                "microcluster_info_signed_url": campaign.get(
                    "microcluster_info_signed_url"
                ),
            }

            url_key_to_downloaded_file_path = {}
            for url_key, signed_url in signed_urls.items():
                if signed_url is None:
                    url_key_to_downloaded_file_path[url_key] = None
                    continue
                current_time = datetime.datetime.now()
                random_uuid = uuid4().hex
                temp_file_prefix = "al_{}_{}_{}_{}".format(
                    current_time.strftime("%Y%m%d_%H%M%S_%f"),
                    str(campaign.get("id")),
                    url_key,
                    random_uuid,
                )
                file_path = self._save_content_to_temp(
                    temp_file_prefix,
                    lambda x: self.download_to_file(signed_url, x),
                    mode="wb",
                )
                url_key_to_downloaded_file_path[url_key] = file_path

            path_key_to_downloaded_file_path = {
                k[:-10] + "path": v for k, v in url_key_to_downloaded_file_path.items()
            }

            # Load data into agent for each campaign
            agent = self.camp_id_to_sample_agent[campaign.get("id")]
            agent.load_sampling_dataset(
                element_type=campaign.get("element_type"),
                preprocessed_info=path_key_to_downloaded_file_path,
            )

    def sample_probabilities(self, frames: List[LabeledFrame]) -> None:
        """Takes a list of Labeled Frames and stores scores for each based on each synced collection campaigns

        Args:
            frames (List[LabeledFrame]): a List of Labeled frames to score based on synced Collection Campaigns
        """
        print("Sampling frames...")

        batch_uuid = uuid4().hex
        self.frame_batch_uuid_to_camp_id_to_probability_score_info[batch_uuid] = {}

        for campaign in self.active_coll_camp_summaries:
            print(f"Scoring frames for campaign id {campaign['id']}...")
            self.frame_batch_uuid_to_camp_id_to_probability_score_info[batch_uuid][
                campaign["id"]
            ] = [
                # A dict with fields (similarity_score, similarity_score_version, sampled_element_id)
                self.camp_id_to_sample_agent[campaign["id"]].score_frame(frame)
                for frame in tqdm(frames, desc="Num frames scored")
            ]

        current_time = datetime.datetime.now()
        temp_frame_prefix = "al_{}_collection_campaign_candidate_frames_{}_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f"), batch_uuid
        )
        frame_path = self._save_content_to_temp(
            temp_frame_prefix,
            lambda x: self.write_to_file([frame.to_dict() for frame in frames], x),
        )
        self.frame_batch_uuid_to_temp_file_path[batch_uuid] = frame_path

        print("Sampling complete!")

        return self.frame_batch_uuid_to_camp_id_to_probability_score_info[batch_uuid]

    def save_for_collection(self, score_threshold: float = 0.5) -> None:
        """Based on the score threshold, take all sampled frames and upload those that score above
        the score threshold for each Collection Campaign.

        Args:
            score_threshold (float, optional): Score threshold for all campaigns to save to server. Defaults to 0.5.
        """
        num_frame_batches = len(self.frame_batch_uuid_to_temp_file_path.keys())

        for idx, frame_batch_uuid in enumerate(
            self.frame_batch_uuid_to_temp_file_path.keys()
        ):
            print(f"Processing frame batch {idx + 1} of {num_frame_batches}...")

            frames = self._read_rows_from_disk(
                self.frame_batch_uuid_to_temp_file_path[frame_batch_uuid]
            )
            camp_id_to_probability_score_info = (
                self.frame_batch_uuid_to_camp_id_to_probability_score_info[
                    frame_batch_uuid
                ]
            )
            for campaign in self.active_coll_camp_summaries:
                scores = camp_id_to_probability_score_info[campaign["id"]]
                filtered_frame_indexes_and_scores = filter(
                    lambda score: score[1].get("similarity_score") >= score_threshold,
                    enumerate(scores),
                )
                filtered_frame_indexes = map(
                    lambda score: score[0], filtered_frame_indexes_and_scores
                )
                filtered_frames_dict = []
                for idx in filtered_frame_indexes:
                    frame_dict = frames[idx]
                    frame_dict["similarity_score"] = scores[idx].get("similarity_score")
                    frame_dict["sampled_element_id"] = scores[idx].get(
                        "sampled_element_id"
                    )
                    frame_dict["similarity_score_version"] = scores[idx].get(
                        "similarity_score_version"
                    )
                    filtered_frames_dict.append(frame_dict)

                if len(filtered_frames_dict) == 0:
                    continue

                print(f"Uploading Frames for Collection Campaign ID {campaign['id']}")
                dataframe_urls = self._upload_collection_frames_to_gcs(
                    frame_batch_uuid, campaign["id"], filtered_frames_dict
                )

                if campaign["id"] not in self.camp_id_to_gcs_frame_urls:
                    self.camp_id_to_gcs_frame_urls[campaign["id"]] = dataframe_urls
                else:
                    self.camp_id_to_gcs_frame_urls[campaign["id"]].extend(
                        dataframe_urls
                    )

        # Now create the collection frames
        for campaign in self.active_coll_camp_summaries:
            if campaign["id"] in self.camp_id_to_gcs_frame_urls:
                payload = {
                    "collection_campaign_id": campaign["id"],
                    "issue_uuid": campaign["issue_uuid"],
                    "dataframe_urls": self.camp_id_to_gcs_frame_urls[campaign["id"]],
                }
                resp = self._post_collection_frames(payload)
                print(resp["message"])
            else:
                print(f"No samples matched for Collection Campaign ID {campaign['id']}")

        mark_temp_directory_complete(self.temp_file_path)
