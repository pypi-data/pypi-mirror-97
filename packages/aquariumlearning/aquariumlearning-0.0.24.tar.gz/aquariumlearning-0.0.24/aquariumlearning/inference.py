"""inference.py
============
The inference and inference frame modules.
"""

import datetime
import json
from io import IOBase
from tempfile import NamedTemporaryFile
import pyarrow as pa
import numpy as np
import pandas as pd
from typing import Any, Optional, Union, Callable, List, Dict, Tuple

from .util import (
    _is_one_gb_available,
    add_object_user_attrs,
    create_temp_directory,
    mark_temp_directory_complete,
    POLYGON_VERTICES_KEYS,
    KEYPOINT_KEYS,
    MAX_FRAMES_PER_BATCH,
)


class InferencesFrame:
    """A frame containing inferences from an experiment.

    Args:
        frame_id (str): A unique id for this frame.
    """

    def __init__(self, *, frame_id: str = None) -> "InferencesFrame":
        if not isinstance(frame_id, str):
            raise Exception("frame ids must be strings")

        if "/" in frame_id:
            raise Exception("frame ids cannot contain slashes (/)")

        self.frame_id = frame_id
        self.inference_data = []
        self.embedding = None
        self.custom_metrics = {}
        self._label_ids_set = set()

    def _set_embedding_structure(self, model_id: str = "") -> None:
        """Sets the internal embedding structure on first add

        Args:
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        self.embedding = {
            "image_url": "",
            "task_id": self.frame_id,
            "crop_embeddings": [],
            "model_id": model_id,
            "date_generated": str(datetime.datetime.now()),
            "embedding": [],
        }

    def add_crop_embedding(
        self, *, label_id: str, embedding: List[float], model_id: str = ""
    ) -> None:
        """Add a per inference crop embedding

        Args:
            label_id (str): [description]
            embedding (List[float]): A vector of floats between length 0 and 12,000.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        if not embedding or len(embedding) > 12000:
            raise Exception("Length of embeddings should be between 0 and 12,000")

        if not self.embedding:
            self._set_embedding_structure(model_id=model_id)

        self.embedding["crop_embeddings"].append(
            {"uuid": label_id, "embedding": embedding}
        )
        self._label_ids_set.add(label_id)

    def add_frame_embedding(
        self, *, embedding: List[float], model_id: str = ""
    ) -> None:
        """Add an embedding to this frame

        Args:
            embedding (List[float]): A vector of floats between length 0 and 12,000.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        if not embedding or len(embedding) > 12000:
            raise Exception("Length of embeddings should be between 0 and 12,000")

        if not self.embedding:
            self._set_embedding_structure(model_id=model_id)

        self.embedding["embedding"] = embedding

    def add_embedding(
        self,
        *,
        embedding: List[float],
        crop_embeddings: Optional[Dict[str, any]] = None,
        model_id: str = "",
    ) -> None:
        """DEPRECATED! PLEASE USE add_frame_embedding and add_crop_embedding
        Add an embedding to this frame, and optionally to crops/labels within it.

        If provided, "crop_embeddings" is a list of dicts of the form:
            'uuid': the label id for the crop/label
            'embedding': a vector of floats between length 0 and 12,000.

        Args:
            embedding (list of floats): A vector of floats between length 0 and 12,000.
            crop_embeddings (list of dicts, optional): A list of dictionaries representing crop embeddings. Defaults to None.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """

        if crop_embeddings is None:
            crop_embeddings = []

        if not embedding or len(embedding) > 12000:
            raise Exception("Length of embeddings should be between 0 and 12,000")

        self.embedding = {
            "image_url": "",
            "task_id": self.frame_id,
            "crop_embeddings": crop_embeddings,
            "model_id": model_id,
            "date_generated": str(datetime.datetime.now()),
            "embedding": embedding,
        }

    def add_custom_metric(
        self, name: str, value: Union[float, List[Union[int, float]]]
    ):
        """Add a custom metric for a given inference frame.

        Args:
            name (str): The name of the custom metric being added. Must match one of the custom_metrics already defined by the corresponding Project.
            value (Union[float, List[Union[int, float]]]): The value of the custom metric (either a float or 2d list of floats/integers).
        """
        if not (isinstance(value, float) or isinstance(value, list)):
            raise Exception(
                "Custom metrics values must be either a float, or a 2D list of floats/integers."
            )

        self.custom_metrics[name] = value

    def _all_label_classes(self) -> List[str]:
        return list(
            set(
                [
                    data["label"]
                    for data in self.inference_data
                    if data["label"] != "__mask"
                ]
            )
        )

    def add_inference_2d_bbox(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        confidence: float,
        area: Optional[float] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an inference for a 2D bounding box.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            area (float, optional): The area of the image.
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "confidence": confidence,
        }
        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd
        # TODO: This is mostly legacy for vergesense
        if area is not None:
            attrs["area"] = area

        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "BBOX_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_text_token(
        self,
        *,
        sensor_id: str,
        label_id: str,
        index: str,
        token: str,
        classification: str,
        visible: bool,
        confidence: float,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a text token.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            index (int): the index of this token in the text
            token (str): the text content of this token
            classification (str): the classification string
            visible (bool): is this a visible token in the text
            confidence (float): confidence of prediction
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {
            "index": index,
            "token": token,
            "visible": visible,
            "confidence": confidence,
        }

        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "TEXT_TOKEN",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_3d_cuboid(
        self,
        *,
        label_id: str,
        classification: str,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        confidence: float,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None,
        coord_frame_id: Optional[str] = None,
    ) -> None:
        """Add an inference for a 3D cuboid.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            position (list of float): the position of the center of the cuboid
            dimensions (list of float): the dimensions of the cuboid
            rotation (list of float): the local rotation of the cuboid, represented as an xyzw quaternion.
            confidence (float): confidence of prediction
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
            coord_frame_id (str, optional): Coordinate frame id. Defaults to 'world'
        """
        if coord_frame_id is None:
            coord_frame_id = "world"

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "dim_x": dimensions[0],
            "dim_y": dimensions[1],
            "dim_z": dimensions[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
            "rot_w": rotation[3],
            "confidence": confidence,
        }

        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        add_object_user_attrs(attrs, user_attrs)

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CUBOID_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_2d_keypoints(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        keypoints: List[Dict[KEYPOINT_KEYS, Union[int, float, str]]],
        confidence: float,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an inference for a 2D keypoints task.

        A keypoint is a dictionary of the form:
            'x': x-coordinate in pixels
            'y': y-coordinate in pixels
            'name': string name of the keypoint

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            keypoints (list of dicts): The keypoints of this detection
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "keypoints": keypoints,
            "confidence": confidence,
        }

        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "KEYPOINTS_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_2d_polygon_list(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Tuple[Union[int, float]]]]],
        confidence: float,
        center: Optional[List[Union[int, float]]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an inference for a 2D polygon list instance segmentation task.

        Polygons are dictionaries of the form:
            'vertices': List of (x, y) vertices (e.g. [[x1,y1], [x2,y2], ...])
                The polygon does not need to be closed with (x1, y1).
                As an example, a bounding box in polygon representation would look like:

                .. code-block::

                    {
                        'vertices': [
                            [left, top],
                            [left + width, top],
                            [left + width, top + height],
                            [left, top + height]
                        ]
                    }


        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            polygons (list of dicts): The polygon geometry
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            center (list of ints or floats, optional): The center point of the instance
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {"polygons": polygons, "center": center, "confidence": confidence}

        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "POLYGON_LIST_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_2d_semseg(
        self, *, sensor_id: str, label_id: str, mask_url: str
    ) -> None:
        """Add an inference for 2D semseg.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            mask_url (str): URL to the pixel mask png.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label": "__mask",
                "label_coordinate_frame": sensor_id,
                "label_type": "SEMANTIC_LABEL_URL_2D",
                "attributes": {"url": mask_url},
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_2d_classification(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        confidence: float,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an inference for 2D classification.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {"confidence": confidence}
        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def add_inference_3d_classification(
        self,
        *,
        label_id: str,
        classification: str,
        confidence: float,
        coord_frame_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for 3D classification.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            coord_frame_id (optional, str): The coordinate frame id.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if coord_frame_id is None:
            coord_frame_id = "world"

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        if not isinstance(confidence, float):
            raise Exception("confidence must be floats")

        attrs = {"confidence": confidence}
        add_object_user_attrs(attrs, user_attrs)

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": attrs,
            }
        )
        self._label_ids_set.add(label_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert this frame into a dictionary representation.

        Returns:
            dict: dictified frame
        """
        row = {"task_id": self.frame_id, "inference_data": self.inference_data}
        row["custom_metrics"] = self.custom_metrics

        return row

    def _to_summary(self) -> Dict[str, Any]:
        """Converts this frame to a lightweight summary dict for internal cataloging

        Returns:
            dict: lightweight summaried frame
        """
        label_counts = {}
        for label in self.inference_data:
            if not label_counts.get(label["label_type"]):
                label_counts[label["label_type"]] = 0
            label_counts[label["label_type"]] += 1
        row = {
            "frame_id": self.frame_id,
            "label_counts": label_counts,
            "custom_metrics_names": self.custom_metrics.keys(),
        }

        return row


class Inferences:
    """A container used to construct a set of inferences.

    Typical usage is to create an Inferences object, add multiple InferencesFrames to it,
    then serialize the frames to be submitted.
    """

    def __init__(self) -> "Inferences":
        if not _is_one_gb_available():
            raise OSError(
                "Attempting to run with less than 1 GB of available disk space. Exiting..."
            )
        self._frames = []
        self._frame_ids_set = set()
        self._label_ids_set = set()
        self._label_classes_set = set()
        self._frame_summaries = []
        current_time = datetime.datetime.now()
        self.temp_file_path = create_temp_directory()
        self._temp_frame_prefix = "al_{}_inference_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_inference_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []

    def _cleanup_temp_dir(self):
        mark_temp_directory_complete(self.temp_file_path)

    def _save_rows_to_temp(
        self, file_name_prefix: str, writefunc: Callable, mode: str = "w"
    ) -> Optional[str]:
        """[summary]

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush inferences to disk with less than 1 GB of available disk space. Exiting..."
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

    def _flush_to_disk(self) -> None:
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if len(self._frames) == 0:
            return
        frame_path = self._save_rows_to_temp(
            self._temp_frame_prefix, lambda x: self.write_to_file(x)
        )
        if frame_path:
            self._temp_frame_file_names.append(frame_path)
        embeddings_path = self._save_rows_to_temp(
            self._temp_frame_embeddings_prefix,
            lambda x: self.write_embeddings_to_file(x),
            mode="wb",
        )
        if embeddings_path:
            self._temp_frame_embeddings_file_names.append(embeddings_path)
        self._frames = []

    def _validate_frame(
        self, frame_summary: Dict[str, Any], project_info: Dict[str, Any]
    ) -> None:
        """Validates single frame in set according to project constraints

        Args:
            frame_summary Dict[str, Any]: dictionary representation of an InferencesFrame summary
            project_info Dict[str, Any]: metadata about the project being uploaded to
        """

        frame_id = frame_summary["frame_id"]
        primary_task = project_info.get("primary_task")
        if primary_task == "2D_SEMSEG":
            label_counts = frame_summary["label_counts"]

            # 2D_SEMSEG frames may only have one label of type SEMANTIC_LABEL_URL_2D
            if (
                len(label_counts) != 1
                or label_counts.get("SEMANTIC_LABEL_URL_2D", 0) != 1
            ):
                extra_labels = filter(
                    lambda x: x != "SEMANTIC_LABEL_URL_2D", label_counts.keys()
                )
                issue_text = (
                    "has no labels"
                    if not len(label_counts)
                    else f"has inference types of {list(extra_labels)}"
                )

                raise Exception(
                    f"Frame {frame_id} {issue_text}. Inferences frames for 2D_SEMSEG projects must have exactly one 2d_semseg inference"
                )

        project_custom_metrics_names = [
            custom_metric["name"]
            for custom_metric in project_info.get("custom_metrics", []) or []
        ]

        for inference_custom_metric_name in frame_summary["custom_metrics_names"]:
            if inference_custom_metric_name not in project_custom_metrics_names:
                potential_candidates_text = ""

                if not len(project_custom_metrics_names):
                    potential_candidates_text = (
                        "No custom metrics have been configured for this project"
                    )

                elif len(project_custom_metrics_names) < 11:
                    potential_candidates_text = (
                        "This project does have the following custom metrics: "
                        f"{', '.join(project_custom_metrics_names)}"
                    )
                else:
                    potential_candidates_text = (
                        "This project includes the following custom metrics: "
                        f"{', '.join(project_custom_metrics_names[:10])}. A full list is returned from calling get_project."
                    )

                raise Exception(
                    f"Frame {frame_id} contains a custom metric {inference_custom_metric_name} that is not configured "
                    f"for project {project_info['id']}. {potential_candidates_text}"
                )

    def _validate_frames(self, project_info: Dict[str, Any]) -> None:
        """Validates all frames in set according to project constraints

        Args:
            project_info Dict[str, Any]: metadata about the project being uploaded to
        """
        for frame_summary in self._frame_summaries:
            self._validate_frame(frame_summary, project_info)

    def add_frame(self, frame: InferencesFrame) -> None:
        """Add an InferencesFrame to this dataset.

        Args:
            frame (InferencesFrame): An InferencesFrame in this dataset.
        """
        if not isinstance(frame, InferencesFrame):
            raise Exception("Frame is not an InferencesFrame")

        if frame.frame_id in self._frame_ids_set:
            raise Exception("Attempted to add duplicate frame id.")

        duplicate_label_ids = frame._label_ids_set & self._label_ids_set
        if duplicate_label_ids:
            raise Exception(
                f"Attempted to add duplicate label id(s): {duplicate_label_ids}"
            )

        self._frames.append(frame)
        self._frame_ids_set.add(frame.frame_id)
        self._label_ids_set.update(frame._label_ids_set)
        self._label_classes_set.update(frame._all_label_classes())
        self._frame_summaries.append(frame._to_summary())
        if len(self._frames) >= MAX_FRAMES_PER_BATCH:
            self._flush_to_disk()

    def write_to_file(self, filelike: IOBase) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        for frame in self._frames:
            row = frame.to_dict()
            filelike.write(json.dumps(row) + "\n")

    def write_embeddings_to_file(self, filelike: IOBase) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # Get the first frame embedding dimension
        frame_embedding_dim = len(self._frames[0].embedding["embedding"])
        # Get the first crop embedding dimension
        crop_embedding_dim = 1
        for frame in self._frames:
            if frame.embedding["crop_embeddings"]:
                first_crop_emb = frame.embedding["crop_embeddings"][0]
                crop_embedding_dim = len(first_crop_emb["embedding"])
                break

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_ids[i] = frame.embedding["task_id"]
            frame_embeddings[i] = frame.embedding["embedding"]
            crop_ids[i] = [x["uuid"] for x in frame.embedding["crop_embeddings"]]
            crop_embeddings[i] = [
                x["embedding"] for x in frame.embedding["crop_embeddings"]
            ]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()
