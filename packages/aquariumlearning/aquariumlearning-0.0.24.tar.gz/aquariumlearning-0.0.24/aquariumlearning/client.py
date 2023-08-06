"""client.py
============
The main client module.
"""

import os
import datetime
import time
from requests.exceptions import ConnectionError
from uuid import uuid4
from io import BytesIO
from google.resumable_media.requests import ResumableUpload
from google.resumable_media.common import InvalidResponse, DataCorruption
from tqdm import tqdm
import sys
from .viridis import viridis_rgb
from .turbo import turbo_rgb
from .issues import IssueManager
from .datasharing import check_urls, get_mode, get_errors
import re
from typing import Any, Optional, Union, List, Dict, Tuple

from .util import (
    _upload_local_files,
    requests_retry,
    assert_valid_name,
    MAX_CHUNK_SIZE,
    raise_resp_exception_error,
)

# All imports here necessary for referenceing and compatiblity
from .dataset import LabeledDataset, LabeledFrame
from .inference import Inferences, InferencesFrame
from .class_map import (
    LabelClassMap,
    ClassMapEntry,
    ClassMapUpdateEntry,
    tableau_colors,
    orig_label_color_list,
)


class StratifiedMetricsDefinition:
    """Definitions for stratified metrics given object-level attributes

    Args:
        name (str): The name of this attribute, which should match the attribute on object labels.
        ordered_values (List[str]): The ordered list of valid values to group by.
    """

    def __init__(
        self, name: str, ordered_values: List[str]
    ) -> "StratifiedMetricsDefinition":
        self.name = name
        self.ordered_values = list(ordered_values)  # In case it's a tuple

    def to_dict(self) -> Dict[str, Union[List[str], str]]:
        return {"name": self.name, "ordered_values": self.ordered_values}


class CustomMetricsDefinition:
    """Definitions for custom user provided metrics.

    Args:
        name (str): The name of this metric.
        metrics_type (str): The metrics type, either 'objective' or 'confusion_matrix'.
    """

    OBJECTIVE = "objective"
    CONFUSION_MATRIX = "confusion_matrix"

    def __init__(self, name, metrics_type: str) -> "CustomMetricsDefinition":
        valid_metrics_types = set(["objective", "confusion_matrix"])
        self.name = name
        self.metrics_type = metrics_type

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "metrics_type": self.metrics_type}


class Client:
    """Client class that interacts with the Aquarium REST API.

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    def __init__(
        self,
        *,
        api_endpoint: str = "https://illume.aquariumlearning.com/api/v1",
        **kwargs,
    ) -> "Client":
        self._creds_token = None
        self._creds_app_id = None
        self._creds_app_key = None
        self._creds_api_key = None
        self.api_endpoint = api_endpoint

    def _get_creds_headers(self) -> Dict[str, str]:
        """Get appropriate request headers for the currently set credentials.

        Raises:
            Exception: No credentials set.

        Returns:
            dict: Dictionary of headers
        """
        if self._creds_token:
            return {"Authorization": "Bearer {token}".format(token=self._creds_token)}
        elif self._creds_api_key:
            return {"x-illume-api-key": self._creds_api_key}
        elif self._creds_app_id and self._creds_app_key:
            return {
                "x-illume-app": self._creds_app_id,
                "x-illume-key": self._creds_app_key,
            }
        else:
            raise Exception("No credentials set.")

    def set_credentials(
        self,
        *,
        token: Optional[str] = None,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """Set credentials for the client.

        Args:
            api_key (str, optional): A string for a long lived API key. Defaults to None.
            token (str, optional): A JWT providing auth credentials. Defaults to None.
            app_id (str, optional): Application ID string. Defaults to None.
            app_key (str, optional): Application secret key. Defaults to None.

        Raises:
            Exception: Invalid credential combination provided.
        """
        if api_key is not None:
            self._creds_api_key = api_key
        elif token is not None:
            self._creds_token = token
        elif app_id is not None and app_key is not None:
            self._creds_app_id = app_id
            self._creds_app_key = app_key
        else:
            raise Exception(
                "Please provide either an api_key, token, or app_id and app_key"
            )

    def _format_error_logs(self, raw_error_logs: List[Dict[str, str]]) -> List[str]:
        """Format error log data into strings.

        Args:
            raw_error_logs (list[dict]): Error log data.

        Returns:
            list[str]: list of string formatted error messages.
        """
        formatted_lines = []
        for raw in raw_error_logs:
            formatted_lines.append(
                f"    {raw.get('aquarium_dataflow_step', '')}: {raw.get('msg', '')}"
            )
        return formatted_lines

    def get_issue_manager(self, project_id: str) -> IssueManager:
        """Get an issue manager object.

        Args:
            project_id (str): Project ID to manage.

        Returns:
            IssueManager: The issue manager object.
        """
        return IssueManager(self, project_id)

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get info about existing projects

        Returns:
            list of dict: Project Info
        """
        r = requests_retry.get(
            self.api_endpoint + "/projects", headers=self._get_creds_headers()
        )

        raise_resp_exception_error(r)
        return r.json()

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get detailed info about a specific project

        Returns:
            Dict[str, Any]: detailed info about a project
        """
        r = requests_retry.get(
            self.api_endpoint + "/projects/" + project_id,
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return r.json()

    def delete_project(self, project_id: str) -> None:
        """Mark a project for deletion

        Args:
            project_id (str): project_id
        """
        if not self.project_exists(project_id):
            raise Exception("Project {} does not exist.".format(project_id))

        url = self.api_endpoint + "/projects/{}".format(project_id)
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def project_exists(self, project_id: str) -> bool:
        """Checks whether a project exists.

        Args:
            project_id (str): project_id

        Returns:
            bool: Does project exist
        """
        projects = self.get_projects()
        existing_project_ids = [project["id"] for project in projects]
        return project_id in existing_project_ids

    def create_project(
        self,
        project_id: str,
        label_class_map: LabelClassMap,
        primary_task: Optional[str] = None,
        secondary_labels=None,
        frame_links: Optional[List[str]] = None,
        label_links: Optional[List[str]] = None,
        default_camera_target: Optional[List[float]] = None,
        default_camera_position: Optional[List[float]] = None,
        custom_metrics: Optional[
            Union[CustomMetricsDefinition, List[CustomMetricsDefinition]]
        ] = None,
        max_shown_categories: Optional[int] = None,
        stratified_metrics: Optional[List[StratifiedMetricsDefinition]] = None,
        include_no_gt: Optional[bool] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a new project via the REST API.

        Args:
            project_id (str): project_id
            label_class_map (LabelClassMap): The label class map used to interpret classifications.
            primary_task (Optional[str], optional): Any specific primary task for a non-object detection or classification task. Can be '2D_SEMSEG' or 'CLASSIFICATION' or None.
            secondary_labels ([type], optional): List of secondary labels in classification tasks
            frame_links (Optional[List[str]], optional): List of string keys for links between frames
            label_links (Optional[List[str]], optional): List of string keys for links between labels
            default_camera_target (Optional[List[float]], optional): For 3D scenes, the default camera target
            default_camera_position (Optional[List[float]], optional): For 3D scenes, the default camera position
            custom_metrics (Optional[ Union[CustomMetricsDefinition, List[CustomMetricsDefinition]] ], optional): Defines which custom metrics exist for this project, defaults to None.
            max_shown_categories (Optional[int], optional): For categorical visualizations, set the maximum shown simultaneously. Max 100.
            stratified_metrics (Optional[List[StratifiedMetricsDefinition]], optional): Defines what object-level attributes to stratify metrics over.
            external_metadata (Optional[Dict[str, Any]], optional): A JSON object that can be used to attach metadata to the project itself
        """

        assert_valid_name(project_id)

        if not isinstance(label_class_map, LabelClassMap):
            raise Exception("label_class_map must be a LabelClassMap")

        if not label_class_map.entries:
            raise Exception("label_class_map must have at least one class")

        dumped_classmap = [x.to_dict() for x in label_class_map.entries]
        payload = {"project_id": project_id, "label_class_map": dumped_classmap}

        if primary_task is not None:
            payload["primary_task"] = primary_task
        if secondary_labels is not None:
            dumped_secondary_labels = []
            for raw in secondary_labels:
                dumped_classmap = [x.to_dict() for x in raw["label_class_map"].entries]
                raw["label_class_map"] = dumped_classmap
                dumped_secondary_labels.append(raw)

            payload["secondary_labels"] = dumped_secondary_labels
        if frame_links is not None:
            if not isinstance(frame_links, list):
                raise Exception("frame_links must be a list of strings")
            payload["frame_links"] = frame_links
        if label_links is not None:
            if not isinstance(label_links, list):
                raise Exception("label_links must be a list of strings")
            payload["label_links"] = label_links
        if default_camera_position is not None:
            if not isinstance(default_camera_position, list):
                raise Exception("default_camera_position must be a list of floats")
            payload["default_camera_position"] = default_camera_position
        if default_camera_target is not None:
            if not isinstance(default_camera_target, list):
                raise Exception("default_camera_target must be a list of floats")
            payload["default_camera_target"] = default_camera_target
        if custom_metrics is not None:
            if isinstance(custom_metrics, CustomMetricsDefinition):
                custom_metrics = [custom_metrics]

            if (
                not custom_metrics
                or (not isinstance(custom_metrics, list))
                or (not isinstance(custom_metrics[0], CustomMetricsDefinition))
            ):
                raise Exception(
                    "custom_metrics must be a CustomMetricsDefinition or list of CustomMetricsDefinition."
                )

            serializable = [x.to_dict() for x in custom_metrics]
            payload["custom_metrics"] = serializable

        if stratified_metrics is not None:
            if (
                not stratified_metrics
                or (not isinstance(stratified_metrics, list))
                or (not isinstance(stratified_metrics[0], StratifiedMetricsDefinition))
            ):
                raise Exception(
                    "stratified_metrics must be a list of StratifiedMetricsDefinition."
                )
            serializable = [x.to_dict() for x in stratified_metrics]
            payload["stratified_metrics"] = serializable

        if max_shown_categories is not None:
            if not isinstance(max_shown_categories, int):
                raise Exception("max_shown_categories must be an int")
            if max_shown_categories < 1 or max_shown_categories > 100:
                raise Exception("max_shown_categories must be between 1 and 100")
            payload["max_shown_categories"] = max_shown_categories

        if include_no_gt is not None:
            payload["include_no_gt"] = include_no_gt

        if external_metadata is not None:
            if not isinstance(external_metadata, dict) or (
                external_metadata and not isinstance(next(iter(external_metadata)), str)
            ):
                raise Exception("external_metadata must be a dict with string keys")
            payload["external_metadata"] = external_metadata

        r = requests_retry.post(
            self.api_endpoint + "/projects",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def _preview_frame_dict(
        self, project_id: str, both_frames_dict: Dict[str, Dict[str, Any]]
    ) -> None:
        """Generate preview with both dataset frame and inference frame as dict

        Args:
            project_id (str): name of project to preview frame with
            both_frames_dict (dict): Dictionary containing the labeled and inference frame
        """
        api_path = "/projects/{}/preview_frame".format(project_id)

        preview_frame_api_root = self.api_endpoint + api_path

        r = requests_retry.post(
            preview_frame_api_root,
            headers=self._get_creds_headers(),
            json=both_frames_dict,
        )
        response_data = r.json()
        if response_data.get("preview_frame_uuid"):
            print("Please visit the following url to preview your frame in the webapp")
            url = (
                self.api_endpoint[:-7]
                + api_path
                + "/"
                + response_data["preview_frame_uuid"]
            )
            print(url)
        else:
            raise Exception(
                "Preview URL could not be constructed by server. "
                "Please make sure you're logged in and check frame data accordingly."
            )

    def preview_frame(
        self,
        project_id: str,
        labeled_frame: LabeledFrame,
        inference_frame: Optional[InferencesFrame] = None,
    ) -> None:
        """prints out a URL that lets you preview a provided frame in the web browser
        Useful for debugging data and image url issues.

        Args:
            project_id (str): Name of project to be associated for this frame preview (for label class association)
            labeled_frame (LabeledFrame): Labeled Frame desired for preview in web-app
            inference_frame (Optional[InferencesFrame], optional): Labeled Inference Desired for preview in web-app. Defaults to None.
        """

        both_frames = {}
        both_frames["labeled_frame"] = labeled_frame.to_dict()
        both_frames["inference_frame"] = (
            inference_frame.to_dict() if inference_frame else None
        )
        self._preview_frame_dict(project_id, both_frames)

    def update_project_metadata(
        self, project_id: str, external_metadata: Dict[str, Any]
    ) -> None:
        """Update project metadata

        Args:
            project_id (str): The project id.
            external_metadata (Dict[Any, Any]): The new metadata
        """
        if not isinstance(external_metadata, dict) or (
            external_metadata and not isinstance(next(iter(external_metadata)), str)
        ):
            raise Exception("external_metadata must be a dict with string keys")

        payload = {"external_metadata": external_metadata}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_id}/metadata",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def update_label_class_map_colors(
        self, project_id: str, changed_label_classes: List[ClassMapUpdateEntry]
    ) -> None:
        """Updates label class colors of a specific project

        Args:
            project_id (str): The project id.
            changed_label_classes (List[ClassMapUpdateEntry]): The list of label classes with changed colors. Must be a subset of the project's overall label class map
        """
        project = self.get_project(project_id)
        label_class_map_dict_by_id = {
            label_class["id"]: label_class for label_class in project["label_class_map"]
        }
        label_class_map_dict_by_name = {
            label_class["name"]: label_class
            for label_class in project["label_class_map"]
        }

        seen_ids = set()
        dumped_changes = []
        for entry in changed_label_classes:
            if not entry.class_id:
                known_label_class = label_class_map_dict_by_name.get(entry.name)
                if not known_label_class:
                    raise Exception(
                        f"Label class with name {entry.name} could not be found in the project's label class map. "
                        "This method only allows changing an existing label class map. "
                        "To append new label classes please use create_project."
                    )
                entry.class_id = known_label_class["id"]

            known_label_class = label_class_map_dict_by_id.get(entry.class_id)

            if not known_label_class:
                raise Exception(
                    f"Label class with id {entry.class_id} could not be found in the project's label class map. "
                    "This method only allows changing an existing label class map. "
                    "To append new label classes please use create_project."
                )

            if entry.class_id in seen_ids:
                raise Exception(
                    f"Label class with id {entry.class_id} ({known_label_class['name']}) has multiple change entries. "
                    "Please consolidate into one change."
                )

            seen_ids.add(entry.class_id)
            dumped_entry = entry.to_dict()

            # lazy shallow None check to avoid overwriting with a null
            dumped_patch_entry = {
                k: v for k, v in dumped_entry.items() if v is not None
            }

            dumped_changes.append(dumped_patch_entry)

        payload = {"label_class_map": dumped_changes}
        r = requests_retry.patch(
            f"{self.api_endpoint}/projects/{project_id}/label_class_map",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def get_datasets(
        self, project_id: str, include_archived: Optional[bool]
    ) -> List[str]:
        """Get existing datasets for a project.

        Args:
            project_id (str): The project id.

        Returns:
            list: A list of dataset info for the project.
        """
        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_id
        )
        params = {"include_archived": include_archived if include_archived else False}
        r = requests_retry.get(
            datasets_api_root, headers=self._get_creds_headers(), params=params
        )
        raise_resp_exception_error(r)
        return r.json()

    def delete_dataset(self, project_id: str, dataset_id: str) -> None:
        """Mark a dataset for deletion

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
        """
        if not self.dataset_exists(project_id, dataset_id):
            raise Exception("Dataset {} does not exist.".format(dataset_id))

        url = self.api_endpoint + "/projects/{}/datasets/{}".format(
            project_id, dataset_id
        )
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def dataset_exists(self, project_id: str, dataset_id: str) -> bool:
        """Check if a dataset exists.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            bool: Whether the dataset already exists.
        """
        datasets = self.get_datasets(project_id, include_archived=True)
        existing_dataset_ids = [dataset.get("id") for dataset in datasets]
        return dataset_id in existing_dataset_ids

    def is_dataset_processed(self, project_id: str, dataset_id: str) -> bool:
        """Check if a dataset is fully processed.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            bool: If the dataset is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/is_processed".format(project_id, dataset_id)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["processed"]

    def get_dataset_ingest_error_logs(
        self, project_id: str, dataset_id: str
    ) -> List[Dict[str, Any]]:
        """Get ingest error log entries for a dataset.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/ingest_error_logs".format(
                project_id, dataset_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed

    def current_dataset_process_state(
        self, project_id: str, dataset_id: str
    ) -> Tuple[str, float]:
        """Current processing state of a dataset.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/process_state".format(project_id, dataset_id)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def current_abstract_dataset_process_step_status(
        self, project_id: str, dataset_id: str
    ) -> Dict[str, Any]:
        """Returns the process steps statuses for a given dataset or inferenceset

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            Dict[str, Any]: A set of process step statuses that exist for a given abstract dataset
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/process_step_status".format(
                project_id, dataset_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed

    @staticmethod
    def parse_normalize_process_step_status(process_step_status_payload):
        return process_step_status_payload["process_step_statuses"]["normalize"][
            "status"
        ]

    def inferences_exists(
        self, project_id: str, dataset_id: str, inferences_id: str
    ) -> bool:
        """Check if a set of inferences exists.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id (str): inferences_id

        Returns:
            bool: Whether the inferences id already exists.
        """
        # TODO: FIXME: We need a first class model for inferences,
        # not just name gluing
        inferences_dataset_id = "_".join(["inferences", dataset_id, inferences_id])
        datasets = self.get_datasets(project_id, include_archived=True)
        existing_dataset_ids = [dataset.get("id") for dataset in datasets]
        return inferences_dataset_id in existing_dataset_ids

    def is_inferences_processed(
        self, project_id: str, dataset_id: str, inferences_id: str
    ) -> bool:
        """Check if a set of inferences is fully processed.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            bool: If the inferences set is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/is_processed".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["processed"]

    def get_inferences_ingest_error_logs(
        self, project_id: str, dataset_id: str, inferences_id: str
    ) -> List[Dict[str, Any]]:
        """Get ingest error log entries for an inference set.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/ingest_error_logs".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed

    def current_inferences_process_state(
        self, project_id: str, dataset_id: str, inferences_id: str
    ) -> Tuple[str, float]:
        """current processing state of inferences.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/process_state".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def upload_asset_from_filepath(
        self, project_id: str, dataset_id: str, filepath: str
    ) -> str:
        """Upload an asset from a local file path.
        This is useful in cases where you have data on your local machine that you want to mirror in aquarium.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            filepath (str): The filepath to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """

        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )

        upload_filename = os.path.basename(filepath)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url = urls["download_url"]

        with open(filepath, "rb") as f:
            upload_resp = requests_retry.put(put_url, data=f)

        raise_resp_exception_error(upload_resp)
        return download_url

    def upload_asset_from_url(
        self, project_id: str, dataset_id: str, source_url: str
    ) -> str:
        """Upload an asset from a private url.
        This is useful in cases where you have data easily accessible on your network that you want to mirror in aquarium.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            source_url (str): The source url to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )

        upload_filename = os.path.basename(source_url)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url = urls["download_url"]

        dl_resp = requests_retry.get(source_url)
        payload = BytesIO(dl_resp.content)

        upload_resp = requests_retry.put(put_url, data=payload)

        raise_resp_exception_error(upload_resp)
        return download_url

    def _upload_rows_from_files(
        self,
        project_id: str,
        dataset_id: str,
        upload_prefix: str,
        upload_suffix: str,
        file_names: List[str],
        delete_after_upload: bool = True,
    ) -> None:
        # Get upload / download URLs
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )

        download_urls = _upload_local_files(
            file_names,
            get_upload_path,
            self._get_creds_headers(),
            upload_prefix,
            upload_suffix,
            delete_after_upload=delete_after_upload,
        )

        return download_urls

    def create_dataset(
        self,
        project_id: str,
        dataset_id: str,
        data_url: Optional[str] = None,
        embeddings_url: Optional[str] = None,
        dataset: Optional[LabeledDataset] = None,
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        embedding_distance_metric: str = "euclidean",
        preview_first_frame: bool = False,
        delete_cache_files_after_upload: bool = True,
        check_first_frame: bool = True,
        external_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a dataset with the provided data urls.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            data_url (Optional[str], optional): A URL to the serialized dataset entries.
            embeddings_url (Optional[str], optional): A URL to the serialized dataset embeddings. Defaults to None.
            dataset (Optional[LabeledDataset], optional): The LabeledDataset to upload.
            wait_until_finish (bool, optional): Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout (datetime.timedelta, optional): Maximum time to wait for. Defaults to 2 hours.
            embedding_distance_metric (str, optional): Distance metric to use for embedding layout. Can be a member of ['euclidean', 'cosine']. Defaults to 'euclidean'.
            preview_first_frame (bool, optional): preview the first frame of the dataset in the webapp before continuing. Requires interaction.
            delete_cache_files_after_upload (bool, optional): flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
            external_metadata (Optional[Dict[str, Any]], optional): A JSON object that can be used to attach metadata to the dataset itself
        """

        assert_valid_name(dataset_id)

        if embedding_distance_metric not in ["euclidean", "cosine"]:
            raise Exception("embedding_distance_metric must be euclidean or cosine.")

        if not isinstance(wait_timeout, datetime.timedelta):
            raise Exception("wait_timeout must be a datetime.timedelta object")

        if self.dataset_exists(project_id, dataset_id):
            raise Exception("Dataset already exists.")

        if dataset:
            dataset._flush_to_disk()

            project_info = self.get_project(project_id)

            dataset._validate_frames(project_info)

            if len(dataset._temp_frame_file_names) == 0:
                raise Exception("Cannot create dataset with 0 frames")

            if preview_first_frame:
                first_frame_dict = dataset.get_first_frame_dict()
                self._preview_frame_dict(
                    project_id,
                    {"labeled_frame": first_frame_dict, "inference_frame": None},
                )
                user_response = input(
                    "Please vist above URL to see your Preview frame.\n\n"
                    "Press ENTER to continue or type `exit` and press ENTER "
                    "to cancel dataset upload.\n"
                )
                if user_response == "exit":
                    print("Canceling dataset upload!")
                    return

            if check_first_frame:
                first_frame_dict = dataset.get_first_frame_dict()
                for sensor in first_frame_dict.get("sensor_data"):
                    urls = list(sensor.get("data_urls").values())
                    local_results = check_urls(urls, None)
                    r = requests_retry.post(
                        self.api_endpoint + "/datasets/verify_urls",
                        headers=self._get_creds_headers(),
                        json={"urls": urls},
                    )
                    server_results = r.json()
                    mode = get_mode(urls, local_results, server_results)
                    errors = get_errors(mode, dataset)

                    if len(errors) > 0:
                        print(f"WARNING! SOME URL ACCESS ERRORS FOUND!")
                        print(f"Errors found: {errors}")
                    else:
                        print("No errors found when checking first frame!")

            project_info = self.get_project(project_id)
            project_label_set = set(
                [label_class["name"] for label_class in project_info["label_class_map"]]
            )
            extra_dataset_labels = dataset._label_classes_set - project_label_set
            if len(extra_dataset_labels) > 0:
                raise Exception(
                    f"Dataset contains labels {extra_dataset_labels} not in project Label Class Map {project_label_set}. "
                    f"Label Class Maps can be updated using append-only logic as specified here. "
                    f"https://aquarium.gitbook.io/aquarium-changelog/changelog-entries/2021-01-22#updating-label-class-maps"
                )

            print("Uploading Labeled Dataset...")
            upload_prefix = "{}_data".format(str(uuid4()))
            upload_suffix = ".jsonl"
            final_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                dataset._temp_frame_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
        elif data_url:
            final_urls = [
                data_url,
            ]
        else:
            raise Exception("Please provide either a data_url or dataset argument")

        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_id
        )
        payload = {
            "dataset_id": dataset_id,
            "data_url": final_urls,
            "embedding_distance_metric": embedding_distance_metric,
            "embedding_upload_version": 1,
        }

        if external_metadata is not None:
            if not isinstance(external_metadata, dict) or (
                external_metadata and not isinstance(next(iter(external_metadata)), str)
            ):
                raise Exception("external_metadata must be a dict with string keys")
            payload["external_metadata"] = external_metadata

        if dataset and dataset._temp_frame_embeddings_file_names:
            print("Uploading Labeled Dataset Embeddings...")
            upload_prefix = "{}_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                dataset._temp_frame_embeddings_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                payload["embeddings_url"] = uploaded_urls
        elif embeddings_url:
            payload["embeddings_url"] = [
                embeddings_url,
            ]

        dataset._cleanup_temp_dir()

        print("Dataset Processing Initiating...")
        r = requests_retry.post(
            datasets_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print("Dataset Processing Initiated Successfully")

        if wait_until_finish:
            print(f"Dataset Processing is waiting on workers to spin up...")
            normalize_status = "PENDING"
            while normalize_status == "PENDING":
                time.sleep(10)
                normalize_status = Client.parse_normalize_process_step_status(
                    self.current_abstract_dataset_process_step_status(
                        project_id, dataset_id
                    )
                )
                full_process_state, _ = self.current_dataset_process_state(
                    project_id, dataset_id
                )
                if full_process_state == "FAILED":
                    print("Dataset processing has failed. Exiting...")
                    return
            print(f"Dataset Processing Workers have been spun up.")
            with tqdm(
                total=100.0,
                file=sys.stdout,
                unit_scale=True,
                desc="Dataset Processing Progress",
            ) as pbar:
                start_time = datetime.datetime.now()
                processing_state = "PENDING"
                display_processing_state = (
                    lambda state: f"Dataset Processing Status: {state}"
                )
                pbar.write(display_processing_state(processing_state))
                while (datetime.datetime.now() - start_time) < wait_timeout:
                    (
                        new_processing_state,
                        new_percent_done,
                    ) = self.current_dataset_process_state(project_id, dataset_id)
                    pbar.update(new_percent_done - pbar.n)
                    if new_processing_state != processing_state:
                        processing_state = new_processing_state
                        pbar.write(display_processing_state(processing_state))
                    processed = self.is_dataset_processed(
                        project_id=project_id, dataset_id=dataset_id
                    )
                    if processed:
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Dataset is fully processed.")
                        break
                    if processing_state == "FAILED":
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Dataset processing has failed. Exiting...")
                        raw_logs = self.get_dataset_ingest_error_logs(
                            project_id, dataset_id
                        )
                        formatted = self._format_error_logs(raw_logs)
                        for entry in formatted:
                            print(entry)

                        break
                    else:
                        time.sleep(10)

                if datetime.datetime.now() - start_time >= wait_timeout:
                    pbar.close()
                    print("Exceeded timeout waiting for job completion.")

    def update_dataset_metadata(
        self, project_id: str, dataset_id: str, external_metadata: Dict[str, Any]
    ) -> None:
        """Update dataset metadata

        Args:
            project_id (str): The project id.
            dataset_id (str): The dataset id.
            external_metadata (Dict[Any, Any]): The new metadata
        """
        if not isinstance(external_metadata, dict) or (
            external_metadata and not isinstance(next(iter(external_metadata)), str)
        ):
            raise Exception("external_metadata must be a dict with string keys")

        payload = {"external_metadata": external_metadata}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_id}/datasets/{dataset_id}/metadata",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    # TODO: Check if the inferences already exist
    def create_inferences(
        self,
        project_id: str,
        dataset_id: str,
        inferences_id: str,
        data_url: Optional[str] = None,
        embeddings_url: Optional[str] = None,
        inferences: Optional[Inferences] = None,
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        embedding_distance_metric: str = "euclidean",
        delete_cache_files_after_upload: bool = True,
        external_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create an inference set with the provided data urls.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id (str): A unique identifier for this set of inferences.
            data_url (Optional[str], optional): A URL to the serialized inference entries.
            embeddings_url (Optional[str], optional): A URL to the serialized inference embeddings. Defaults to None.
            inferences (Optional[Inferences], optional): The inferences to upload.
            wait_until_finish (bool, optional): Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout (datetime.timedelta, optional): Maximum time to wait for. Defaults to 2 hours.
            embedding_distance_metric (str, optional): Distance metric to use for embedding layout. Can be a member of ['euclidean', 'cosine']. Defaults to 'euclidean'.
            delete_cache_files_after_upload (bool, optional): flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
            external_metadata (Optional[Dict[str, Any]], optional): A JSON object that can be used to attach metadata to the inferences itself
        """

        assert_valid_name(dataset_id)
        assert_valid_name(inferences_id)
        queue_after_dataset = True

        if embedding_distance_metric not in ["euclidean", "cosine"]:
            raise Exception("embedding_distance_metric must be euclidean or cosine.")

        if not isinstance(wait_timeout, datetime.timedelta):
            raise Exception("wait_timeout must be a datetime.timedelta object")

        if not self.dataset_exists(project_id, dataset_id):
            raise Exception(f"Dataset {dataset_id} does not exist")
        if (
            not self.is_dataset_processed(project_id, dataset_id)
            and not queue_after_dataset
        ):
            raise Exception(f"Dataset {dataset_id} is not fully processed")
        # If the dataset is already processed, ignore the queue arg
        if self.is_dataset_processed(project_id, dataset_id) and queue_after_dataset:
            queue_after_dataset = False

        if self.inferences_exists(project_id, dataset_id, inferences_id):
            raise Exception("Inferences already exists.")

        inferences_api_root = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences".format(project_id, dataset_id)
        )

        if inferences:
            inferences._flush_to_disk()

            project_info = self.get_project(project_id)
            project_label_set = set(
                [label_class["name"] for label_class in project_info["label_class_map"]]
            )
            extra_inferences_labels = inferences._label_classes_set - project_label_set
            if len(extra_inferences_labels) > 0:
                raise Exception(
                    f"Dataset contains labels {extra_inferences_labels} not in project Label Class Map {project_label_set}"
                )

            inferences._validate_frames(project_info)
            print("Uploading Inferences...")

            upload_prefix = "{}_data".format(str(uuid4()))
            upload_suffix = ".jsonl"
            final_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                inferences._temp_frame_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
        elif data_url:
            final_urls = [
                data_url,
            ]
        else:
            raise Exception("Please provide either a data_url or dataset argument")

        payload = {
            "inferences_id": inferences_id,
            "data_url": final_urls,
            "embedding_distance_metric": embedding_distance_metric,
            "embedding_upload_version": 1,
            "queue_after_dataset": queue_after_dataset,
        }

        if external_metadata is not None:
            if not isinstance(external_metadata, dict) or (
                external_metadata and not isinstance(next(iter(external_metadata)), str)
            ):
                raise Exception("external_metadata must be a dict with string keys")
            payload["external_metadata"] = external_metadata

        if inferences and inferences._temp_frame_embeddings_file_names:
            print("Uploading Inference Embeddings...")
            upload_prefix = "{}_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                inferences._temp_frame_embeddings_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                payload["embeddings_url"] = uploaded_urls
        elif embeddings_url:
            payload["embeddings_url"] = [
                embeddings_url,
            ]

        inferences._cleanup_temp_dir()
        print(f"Inferences Processing Queuing...")

        r = requests_retry.post(
            inferences_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print(f"Inferences Processing Queued Successfully")

        if wait_until_finish:
            total_inferences_id = f"inferences_{dataset_id}_{inferences_id}"
            print(f"Inferences Processing is waiting on workers to spin up...")
            normalize_status = "PENDING"
            while normalize_status == "PENDING":
                time.sleep(10)
                normalize_status = Client.parse_normalize_process_step_status(
                    self.current_abstract_dataset_process_step_status(
                        project_id, total_inferences_id
                    )
                )
                full_process_state, _ = self.current_inferences_process_state(
                    project_id, dataset_id, inferences_id
                )
                if full_process_state == "FAILED":
                    print("Inferences processing has failed. Exiting...")
                    return
            print(f"Inferences Processing Workers have been spun up.")
            with tqdm(
                total=100.0,
                file=sys.stdout,
                unit_scale=True,
                desc="Inferences Processing Progress",
            ) as pbar:
                start_time = datetime.datetime.now()
                processing_state = "PENDING"
                display_processing_state = (
                    lambda state: f"Inferences Processing State: {state}"
                )
                pbar.write(display_processing_state(processing_state))
                while (datetime.datetime.now() - start_time) < wait_timeout:
                    (
                        new_processing_state,
                        new_percent_done,
                    ) = self.current_inferences_process_state(
                        project_id, dataset_id, inferences_id
                    )
                    pbar.update(new_percent_done - pbar.n)
                    if new_processing_state != processing_state:
                        processing_state = new_processing_state
                        pbar.write(display_processing_state(processing_state))
                    processed = self.is_inferences_processed(
                        project_id=project_id,
                        dataset_id=dataset_id,
                        inferences_id=inferences_id,
                    )
                    if processed:
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Inferences are fully processed.")
                        break
                    if processing_state == "FAILED":
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Inferences processing has failed. Exiting...")
                        raw_logs = self.get_inferences_ingest_error_logs(
                            project_id, dataset_id, inferences_id
                        )
                        formatted = self._format_error_logs(raw_logs)
                        for entry in formatted:
                            print(entry)

                        break
                    else:
                        time.sleep(10)

                if datetime.datetime.now() - start_time >= wait_timeout:
                    pbar.close()
                    print("Exceeded timeout waiting for job completion.")

    # Even though this is the same implementation as `update_dataset_metadata`, we split it out
    # because users have been working with inference-specific functions
    def update_inferences_metadata(
        self, project_id: str, inferences_id: str, external_metadata: Dict[str, Any]
    ) -> None:
        """Update dataset metadata

        Args:
            project_id (str): The project id.
            inferences_id (str): The inferences id.
            external_metadata (Dict[Any, Any]): The new metadata
        """
        if not isinstance(external_metadata, dict) or (
            external_metadata and not isinstance(next(iter(external_metadata)), str)
        ):
            raise Exception("external_metadata must be a dict with string keys")

        payload = {"external_metadata": external_metadata}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_id}/datasets/{inferences_id}/metadata",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)
