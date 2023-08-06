"""dataset.py
============
The dataset and dataset frame classes.
"""

import datetime
import json
from io import IOBase
from tempfile import NamedTemporaryFile
import pyarrow as pa
import numpy as np
import pandas as pd
import re
from typing import Any, Optional, Union, Callable, List, Dict, Tuple

from .util import (
    _is_one_gb_available,
    assert_valid_name,
    add_object_user_attrs,
    create_temp_directory,
    mark_temp_directory_complete,
    TYPE_PRIMITIVE_TO_STRING_MAP,
    USER_METADATA_TYPES,
    POLYGON_VERTICES_KEYS,
    POSITION_KEYS,
    ORIENTATION_KEYS,
    KEYPOINT_KEYS,
    MAX_FRAMES_PER_BATCH,
)


class LabeledFrame:
    """A labeled frame for a dataset.

    Args:
        frame_id (str): A unique id for this frame.
        date_captured (str, optional): ISO formatted datetime string. Defaults to None.
        device_id (str, optional): The device that generated this frame. Defaults to None.
    """

    def __init__(
        self,
        *,
        frame_id: str,
        date_captured: Optional[str] = None,
        device_id: Optional[str] = None,
    ) -> "LabeledFrame":
        if not isinstance(frame_id, str):
            raise Exception("frame ids must be strings")

        if "/" in frame_id:
            raise Exception("frame ids cannot contain slashes (/)")

        self.frame_id = frame_id

        if date_captured is not None:
            self.date_captured = date_captured
        else:
            self.date_captured = str(datetime.datetime.now())

        if device_id is not None:
            self.device_id = device_id
        else:
            self.device_id = "default_device"

        self.coordinate_frames = []
        self.sensor_data = []
        self.label_data = []
        self.geo_data = {}
        self.user_metadata = []
        self.embedding = None

        self._coord_frame_ids_set = set()
        self._label_ids_set = set()

    def _add_coordinate_frame(self, coord_frame_obj: Dict[str, str]) -> None:
        """Add coordinate frame to the dataset frame

        Args:
            coord_frame_obj (Dict[str, str]): takes in 'coordinate_frame_id', 'coordinate_frame_type' and optional 'coordinate_frame_metadata'(json dict)
        """
        self.coordinate_frames.append(coord_frame_obj)
        self._coord_frame_ids_set.add(coord_frame_obj["coordinate_frame_id"])

    def _coord_frame_exists(self, coord_frame_id: str):
        """Check to see if the coord frame id is already part of the frame

        Args:
            coord_frame_id (str): The coord frame id to check for inclusion

        Returns:
            bool: whether or not the coord frame id is in the frame set
        """
        return coord_frame_id in self._coord_frame_ids_set

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

    def _all_label_classes(self) -> List[str]:
        return list(
            set(
                [data["label"] for data in self.label_data if data["label"] != "__mask"]
            )
        )

    def add_crop_embedding(
        self, *, label_id: str, embedding: List[float], model_id: str = ""
    ) -> None:
        """Add a per label crop embedding

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

    # TODO: Better datamodel for embeddings, make it more first class
    def add_embedding(
        self,
        *,
        embedding: List[float],
        crop_embeddings: Optional[List[Dict[str, Any]]] = None,
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

    def add_label_text_token(
        self,
        *,
        sensor_id: str,
        label_id: str,
        index: int,
        token: str,
        classification: str,
        visible: bool,
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
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"index": index, "token": token, "visible": visible}
        add_object_user_attrs(attrs, user_attrs)

        self.label_data.append(
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

    # TODO: Dedupe code between here and inferences
    def add_label_3d_cuboid(
        self,
        *,
        label_id: str,
        classification: str,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None,
        coord_frame_id: Optional[str] = None,
    ) -> None:
        """Add a label for a 3D cuboid.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            position (list of float): the position of the center of the cuboid
            dimensions (list of float): the dimensions of the cuboid
            rotation (list of float): the local rotation of the cuboid, represented as an xyzw quaternion.
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
            coord_frame_id (str, optional): Coordinate frame id. Defaults to 'world'
        """
        if coord_frame_id is None:
            coord_frame_id = "world"

        if not self._coord_frame_exists(coord_frame_id):
            raise Exception("Sensor id {} does not exists.".format(coord_frame_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")
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
        }

        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        add_object_user_attrs(attrs, user_attrs)

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.label_data.append(
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

    # TODO: Dedupe code between here and inferences
    def add_label_2d_bbox(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D bounding box.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"top": top, "left": left, "width": width, "height": height}
        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        add_object_user_attrs(attrs, user_attrs)

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.label_data.append(
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

    def add_label_2d_keypoints(
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
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D keypoints task.

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
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "keypoints": keypoints,
        }

        add_object_user_attrs(attrs, user_attrs)

        self.label_data.append(
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

    def add_label_2d_polygon_list(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Tuple[Union[int, float]]]]],
        center: Optional[List[Union[int, float]]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D polygon list instance segmentation task.

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
            center (list of ints or floats, optional): The center point of the instance
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"polygons": polygons, "center": center}

        add_object_user_attrs(attrs, user_attrs)

        self.label_data.append(
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

    def add_label_2d_semseg(
        self, *, sensor_id: str, label_id: str, mask_url: str
    ) -> None:
        """Add a label for 2D semseg.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            mask_url (str): URL to the pixel mask png.
        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        self.label_data.append(
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

    def add_label_2d_classification(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        secondary_labels: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for 2D classification.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            secondary_labels (dict, optional): dictionary of secondary labels
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {}
        if secondary_labels is not None:
            for k, v in secondary_labels.items():
                attrs[k] = v

        add_object_user_attrs(attrs, user_attrs)

        self.label_data.append(
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

    def add_label_3d_classification(
        self,
        *,
        label_id: str,
        classification: str,
        coord_frame_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for 3D classification.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            coord_frame_id (str, optional): The coordinate frame id.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if coord_frame_id is None:
            coord_frame_id = "world"

        if not self._coord_frame_exists(coord_frame_id):
            raise Exception("Coord frame {} does not exists.".format(coord_frame_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {}
        add_object_user_attrs(attrs, user_attrs)

        self.label_data.append(
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

    def add_user_metadata(
        self,
        key: str,
        val: Union[str, int, float, bool],
        val_type: Optional[USER_METADATA_TYPES] = None,
    ) -> None:
        """Add a user provided metadata field.

        The types of these metadata fields will be infered and they'll be made
        available in the app for querying and metrics.

        Args:
            key (str): The key for your metadata field
            val (Union[str, int, float, bool]): value
            val_type (Literal["str", "int", "float", "bool"], optional): type of val as string. Defaults to None.
        """
        assert_valid_name(key)
        # Validates that neither val or type is None
        if val is None and val_type is None:
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata key {key} must provide "
                f"scalar value or expected type of scalar value if None"
            )
        # Validates that val has an accepted type
        if val is not None and type(val) not in TYPE_PRIMITIVE_TO_STRING_MAP:
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata Value {val} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )
        # Validates that val_type has an accepted type
        if val_type and val_type not in TYPE_PRIMITIVE_TO_STRING_MAP.values():
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata Value Type {val_type} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )

        # Sets val_type if it is not set
        if val is not None and not val_type:
            val_type = TYPE_PRIMITIVE_TO_STRING_MAP[type(val)]

        # Checks that inferred type matches what the user put in val_type
        if val is not None:
            for (
                primitive,
                type_string,
            ) in TYPE_PRIMITIVE_TO_STRING_MAP.items():
                if type(val) is primitive and val_type != type_string:
                    raise Exception(
                        f"For frame_id {self.frame_id}, metadata key: {key}, value: {val}, "
                        f"type is inferred as {type_string} but provided type was {val_type}"
                    )

        self.user_metadata.append((key, val, val_type))

    def add_geo_latlong_data(self, lat: float, lon: float) -> None:
        """Add a user provided EPSG:4326 WGS84 lat long pair to each frame

        We expect these values to be floats

        Args:
            lat (float): lattitude of Geo Location
            lon (float): longitude of Geo Location
        """
        if not (isinstance(lat, float) and isinstance(lon, float)):
            raise Exception(
                f"Lattitude ({lat}) and Longitude ({lon}) must both be floats."
            )

        self.geo_data["geo_EPSG4326_lat"] = lat
        self.geo_data["geo_EPSG4326_lon"] = lon

    def add_point_cloud_pcd(
        self,
        *,
        sensor_id: str,
        pcd_url: str,
        coord_frame_id: Optional[str] = None,
        date_captured: Optional[str] = None,
    ) -> None:
        """Add a point cloud sensor data point to this frame,
        contained in PCD format. ascii, binary, and binary_compressed formats are supported.
        Numeric values for the following column names are expected:
        x, y, z, intensity (optional), range (optional)

        Args:
            sensor_id (str): sensor id
            pcd_url (str): URL to PCD formated data
            coord_frame_id (Optional[str], optional): The coordinate frame id. Defaults to None.
            date_captured (Optional[str], optional): ISO formatted date. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "pcd_url": pcd_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            if coord_frame_id == "world":
                self._add_coordinate_frame(
                    {
                        "coordinate_frame_id": coord_frame_id,
                        "coordinate_frame_type": "WORLD",
                    }
                )
            else:
                raise Exception(
                    "Coordinate frame {} does not exist.".format(coord_frame_id)
                )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "POINTCLOUD_PCD_V0",
            }
        )

    def add_point_cloud_bins(
        self,
        *,
        sensor_id: str,
        pointcloud_url: str,
        intensity_url: str,
        range_url: str,
        coord_frame_id: Optional[str] = None,
        date_captured: Optional[str] = None,
    ) -> None:
        """Add a point cloud sensor data point to this frame, contained in dense binary files of
        little-endian values, similar to the raw format of KITTI lidar data.

        Args:
            sensor_id (str): Sensor id
            pointcloud_url (str): URL for the pointcloud: float32 [x1, y1, z1, x2, y2, z2, ...]
            intensity_url (str): URL for the Intensity Pointcloud: unsigned int32 [i1, i2, ...]
            range_url (str): URL for the Range Pointcloud: float32 [r1, r2, ...]
            coord_frame_id (Optional[str], optional): Id for the Coordinate Frame. Defaults to None.
            date_captured (Optional[str], optional): ISO formatted date. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "pointcloud_url": pointcloud_url,
            "range_url": range_url,
            "intensity_url": intensity_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            if coord_frame_id == "world":
                self._add_coordinate_frame(
                    {
                        "coordinate_frame_id": coord_frame_id,
                        "coordinate_frame_type": "WORLD",
                    }
                )
            else:
                raise Exception(
                    "Coordinate frame {} does not exist.".format(coord_frame_id)
                )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "POINTCLOUD_V0",
            }
        )

    def add_obj(
        self,
        *,
        sensor_id: str,
        obj_url: str,
        coord_frame_id: Optional[str] = None,
        date_captured: Optional[str] = None,
    ) -> None:
        """Add a .obj file to the frame for text based geometry

        Args:
            sensor_id (str): sensor id
            obj_url (str): URL to where the object is located
            coord_frame_id (Optional[str], optional): ID for the coordinate frame. Defaults to None.
            date_captured (Optional[str], optional): ISO formatted date. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "obj_url": obj_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            self._add_coordinate_frame(
                {
                    "coordinate_frame_id": coord_frame_id,
                    "coordinate_frame_type": "WORLD",
                }
            )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "OBJ_V0",
            }
        )

    def add_image(
        self,
        *,
        sensor_id: str,
        image_url: str,
        preview_url: Optional[str] = None,
        date_captured: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Add an image "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            image_url (str): The URL to load this image data.
            preview_url (Optional[str], optional): A URL to a compressed version of the image. It must be the same pixel dimensions as the original image. Defaults to None.
            date_captured (Optional[str], optional): ISO formatted date. Defaults to None.
            width (Optional[int], optional): The width of the image in pixels. Defaults to None.
            height (Optional[int], optional): The height of the image in pixels. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        sensor_metadata = {}
        if width is not None:
            if not isinstance(width, int):
                raise Exception("width must be an int")
            sensor_metadata["width"] = width

        if height is not None:
            if not isinstance(height, int):
                raise Exception("height must be an int")
            sensor_metadata["height"] = height

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"image_url": image_url}
        if preview_url is not None:
            data_urls["preview_url"] = preview_url

        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "IMAGE"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": sensor_metadata,
                "sensor_type": "IMAGE_V0",
            }
        )

    def add_audio(
        self,
        *,
        sensor_id: str,
        audio_url: str,
        date_captured: Optional[str] = None,
    ) -> None:
        """Add an audio "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            audio_url (str): The URL to load this audio data (mp3, etc.).
            date_captured (str, optional): ISO formatted date. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        sensor_metadata = {}
        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"audio_url": audio_url}

        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "AUDIO"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": sensor_metadata,
                "sensor_type": "AUDIO_V0",
            }
        )

    def add_coordinate_frame_3d(
        self,
        *,
        coord_frame_id: str,
        position: Optional[Dict[POSITION_KEYS, Union[int, float]]] = None,
        orientation: Optional[Dict[ORIENTATION_KEYS, Union[int, float]]] = None,
        parent_frame_id: Optional[str] = None,
    ) -> None:
        """Add a 3D Coordinate Frame.

        Args:
            coord_frame_id (str): String identifier for this coordinate frame
            position (Optional[Dict[POSITION, Union[int, float]]], optional): Dict of the form {x, y, z}. Defaults to None.
            orientation (Optional[Dict[ORIENTATION, Union[int, float]]], optional): Quaternion rotation dict of the form {w, x, y, z}. Defaults to None.
            parent_frame_id (Optional[str], optional): String id of the parent coordinate frame. Defaults to None.
        """

        if not isinstance(coord_frame_id, str):
            raise Exception("coord_frame_id must be a string")

        if coord_frame_id == "world":
            raise Exception("coord_frame_id cannot be world")

        if self._coord_frame_exists(coord_frame_id):
            raise Exception("Coordinate frame already exists.")

        # If world doesn't exist, make the world coordinate frame
        if not self._coord_frame_exists("world"):
            self._add_coordinate_frame(
                {
                    "coordinate_frame_id": "world",
                    "coordinate_frame_type": "WORLD",
                }
            )

        if position is None:
            position = {"x": 0, "y": 0, "z": 0}

        if orientation is None:
            orientation = {"w": 1, "x": 0, "y": 0, "z": 0}

        if parent_frame_id is None:
            parent_frame_id = "world"

        metadata = {
            "position": position,
            "orientation": orientation,
            "parent_frame_id": parent_frame_id,
        }

        self._add_coordinate_frame(
            {
                "coordinate_frame_id": coord_frame_id,
                "coordinate_frame_type": "WORLD",
                "coordinate_frame_metadata": json.dumps(metadata),
            }
        )

    def add_text(
        self, *, sensor_id: str, text: str, date_captured: Optional[str] = None
    ) -> None:
        """Add a text "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            text (str): The text body.
            date_captured (str, optional): ISO formatted date. Defaults to None.
        """

        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"text": text}
        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "TEXT"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "TEXT",
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert this frame into a dictionary representation.

        Returns:
            dict: dictified frame
        """
        row = {
            "task_id": self.frame_id,
            "date_captured": self.date_captured,
            "device_id": self.device_id,
            "coordinate_frames": self.coordinate_frames,
            "sensor_data": self.sensor_data,
            "label_data": self.label_data,
            "geo_data": self.geo_data,
        }
        user_metadata_types = {}

        for k, v, vt in self.user_metadata:
            namespaced = k
            if "user__" not in namespaced:
                namespaced = "user__" + namespaced
            row[namespaced] = v
            user_metadata_types[namespaced] = vt

        row["user_metadata_types"] = user_metadata_types
        return row

    def _to_summary(self) -> Dict[str, Any]:
        """Converts this frame to a lightweight summary dict for internal cataloging

        Returns:
            dict: lightweight summaried frame
        """
        label_counts = {}
        for label in self.label_data:
            if not label_counts.get(label["label_type"]):
                label_counts[label["label_type"]] = 0
            label_counts[label["label_type"]] += 1
        row = {"frame_id": self.frame_id, "label_counts": label_counts}

        return row


class LabeledDataset:
    """A container used to construct a labeled dataset.

    Typical usage is to create a LabeledDataset, add multiple LabeledFrames to it,
    then serialize the frames to be submitted.
    """

    def __init__(self) -> "LabeledDataset":
        self._frames = []
        self._frame_ids_set = set()
        self._label_ids_set = set()
        self._label_classes_set = set()
        self._frame_summaries = []
        current_time = datetime.datetime.now()
        self.temp_file_path = create_temp_directory()
        self._temp_frame_prefix = "al_{}_dataset_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_dataset_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []

    def _cleanup_temp_dir(self):
        mark_temp_directory_complete(self.temp_file_path)

    def get_first_frame_dict(self) -> Dict[str, Any]:
        first_frame_file_name = self._temp_frame_file_names[0]
        with open(first_frame_file_name, "r") as first_frame_file:
            first_frame_json = first_frame_file.readline().strip()
            return json.loads(first_frame_json)

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
            frame_summary Dict[str, Any]: dictionary representation of a LabeledFrame's summary
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
                    else f"has label types of {list(extra_labels)}"
                )

                raise Exception(
                    f"Frame {frame_id} {issue_text}. Dataset frames for 2D_SEMSEG projects must have exactly one 2d_semseg label"
                )

    def _validate_frames(self, project_info: Dict[str, Any]) -> None:
        """Validates all frames in set according to project constraints

        Args:
            project_info Dict[str, Any]: metadata about the project being uploaded to
        """
        for frame_summary in self._frame_summaries:
            self._validate_frame(frame_summary, project_info)

    def add_frame(self, frame: LabeledFrame) -> None:
        """Add a LabeledFrame to this dataset.

        Args:
            frame (LabeledFrame): A LabeledFrame in this dataset.
        """
        if not isinstance(frame, LabeledFrame):
            raise Exception("Frame is not an LabeledFrame")

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
