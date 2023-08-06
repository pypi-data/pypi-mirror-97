"""API MODEL."""
from typing import List, Mapping, Dict, Optional, Union, Any
from datetime import datetime
import dateutil.parser

from .model.abstract_models import RequestCall, Response
from .model.enums import InputBatchStatus, InvalidatedReasonInput, InputStatus
# To preserve old import statements
from .model.enums import CameraType
from .model.calibration import CameraProperty
from .model.calibration_legacy import CameraCalibration, LidarCalibration
from .model.calibration import CameraCalibrationExplicit, LidarCalibrationExplicit
ENVELOPED_JSON_TAG = "data"


def ts_to_dt(date_string: str) -> datetime:
    return dateutil.parser.parse(date_string)


#
# Request Calls
#


class Image(RequestCall):
    def __init__(self, filename: str,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 source: str = "CAM"):

        self.filename = filename
        self.width = width
        self.height = height
        self.source = source

    def to_dict(self) -> dict:
        return dict(filename=self.filename,
                    width=self.width,
                    height=self.height,
                    source=self.source)


class ImagesFiles(RequestCall):
    def __init__(self, images: List[Image]):
        self.images = images

    def to_dict(self) -> dict:
        return dict(images=[image.to_dict() for image in self.images])


class Video(RequestCall):
    def __init__(self, filename: str,
                 width: int,
                 height: int,
                 source: str = "CAM"):

        self.filename = filename
        self.width = width
        self.height = height
        self.source = source

    def to_dict(self) -> dict:
        return dict(filename=self.filename,
                    width=self.width,
                    height=self.height,
                    source=self.source)


class PointCloud(RequestCall):
    def __init__(self, filename: str, source: Optional[str] = "lidar"):
        self.filename = filename
        self.source = source

    def to_dict(self) -> dict:
        return dict(filename=self.filename,
                    source=self.source)


class PointCloudsWithImages(RequestCall):
    def __init__(self, images: List[Image], point_clouds: List[PointCloud]):
        self.images = images
        self.point_clouds = point_clouds

    def to_dict(self):
        return dict(images=[image.to_dict() for image in self.images],
                    pointClouds=[pc.to_dict() for pc in self.point_clouds])


class PointCloudFiles(RequestCall):
    def __init__(self, point_clouds: List[PointCloud]):
        self.point_clouds = point_clouds

    def to_dict(self) -> dict:
        return dict(pointClouds=[point_cloud.to_dict() for point_cloud in self.point_clouds])


class Calibration(RequestCall):
    def __init__(self, calibration_dict: Dict[str, Union[CameraCalibration, CameraCalibrationExplicit, LidarCalibrationExplicit, LidarCalibration]]):  # noqa:E501
        self.calibration_dict = calibration_dict

    def to_dict(self):
        return dict(
            [(k, v.to_dict()) for (k, v) in self.calibration_dict.items()]
        )


class CalibrationSpec(RequestCall):
    def __init__(self, external_id: str,
                 calibration: Calibration):
        self.external_id = external_id
        self.calibration = calibration

    def to_dict(self):
        return {
            'externalId': self.external_id,
            'calibration': self.calibration.to_dict()
        }


class SourceSpecification(RequestCall):
    def __init__(self, source_to_pretty_name: Optional[Dict[str, str]] = None,
                 source_order: Optional[List[str]] = None):

        self.source_to_pretty_name = source_to_pretty_name
        self.source_order = source_order

    def to_dict(self):
        as_dict = {}
        if self.source_to_pretty_name is not None:
            as_dict['sourceToPrettyName'] = self.source_to_pretty_name
        if self.source_order is not None:
            as_dict['sourceOrder'] = self.source_order

        return as_dict


class SceneMetaData(RequestCall):
    def __init__(
        self, external_id: str, source_specification: Optional[SourceSpecification] = None
    ):
        self.external_id = external_id
        self.source_specification = source_specification

    def to_dict(self):
        as_dict = dict(externalId=self.external_id)
        if self.source_specification is not None:
            as_dict["sourceSpecification"] = self.source_specification.to_dict()
        return as_dict


class CalibratedSceneMetaData(SceneMetaData):
    def __init__(self, external_id: str,
                 calibration_id: int,
                 source_specification: Optional[SourceSpecification] = None):

        super().__init__(external_id, source_specification)
        self.calibration_id = calibration_id

    def to_dict(self):
        as_dict = super().to_dict()
        if self.calibration_id is not None:
            as_dict['calibrationId'] = self.calibration_id

        return as_dict


class TimeCalibration(RequestCall):
    def __init__(self, offset_spec: Dict[str, float]):
        self.offset_spec = offset_spec

    def to_dict(self) -> dict:
        return dict(offsetSpec=self.offset_spec)


class TimeSpecification(RequestCall):
    def __init__(self, start_ts: float, end_ts: float, time_calibration: TimeCalibration):
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.time_calibration = time_calibration

    def to_dict(self) -> dict:

        as_dict: Dict[Any, Any] = dict(timeCalibration=self.time_calibration.to_dict())

        if self.start_ts:
            as_dict["startTs"] = self.start_ts
        if self.end_ts:
            as_dict["endTs"] = self.end_ts

        return as_dict


class SlamDynamicObjects():
    def __init__(self,
                 cuboids: List[str],
                 cuboid_timespans: List[str]
                 ):
        self.cuboids = cuboids
        self.cuboid_timespans = cuboid_timespans

    def to_dict(self):
        return dict(cuboids=self.cuboids, cuboidTimespans=self.cuboid_timespans)


class SlamMetaData(CalibratedSceneMetaData):
    def __init__(self, external_id: str,
                 vehicle_data: List[str],
                 dynamic_objects: SlamDynamicObjects,
                 trajectory: Optional[str],
                 time_specification: TimeSpecification,
                 source_specification: SourceSpecification,
                 calibration_id: int,
                 sequence_id: int,
                 sub_sequence_id: int,
                 settings: Optional[dict] = None):
        super().__init__(external_id, calibration_id, source_specification)
        self.vehicle_data = vehicle_data
        self.dynamic_objects = dynamic_objects
        self.trajectory = trajectory
        self.time_specification = time_specification
        self.sequence_id = sequence_id
        self.sub_sequence_id = sub_sequence_id
        self.settings = settings

    def to_dict(self):
        as_dict = super().to_dict()
        as_dict["vehicleData"] = self.vehicle_data
        as_dict["dynamicObjects"] = self.dynamic_objects.to_dict()
        as_dict["timeSpecification"] = self.time_specification.to_dict()
        as_dict["sequenceId"] = self.sequence_id
        as_dict["subSequenceId"] = self.sub_sequence_id

        if self.settings:
            as_dict["settings"] = self.settings

        if self.trajectory:
            as_dict["trajectory"] = self.trajectory

        return as_dict


class SlamFiles(RequestCall):
    def __init__(self, point_clouds: List[PointCloud], videos: Optional[List[Video]]):
        self.point_clouds = point_clouds
        self.videos = videos

    def to_dict(self):
        as_dict = dict(pointClouds=[pc.to_dict() for pc in self.point_clouds])
        if self.videos is not None:
            as_dict['videos'] = [video.to_dict() for video in self.videos]

        return as_dict


class FilesToUpload(RequestCall):
    """
    Used when retrieving upload urls from input api
    """

    def __init__(self, files: List[str]):
        self.files = files

    def to_dict(self):
        return dict(filesToUpload=self.files)


class PoseTransform(RequestCall):
    def __init__(self, timestamp: int, utc_timestamp: float, position: List[float],
                 rotation_quaternion: List[float]):
        self.timestamp = timestamp
        self.utc_timestamp = utc_timestamp
        self.position = position
        self.rotation_quaternion = rotation_quaternion

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "utc_timestamp": self.utc_timestamp,
            "position": self.position,
            "rotation_quaternion": self.rotation_quaternion
        }


class Trajectory(RequestCall):
    def __init__(self, trajectory: List[PoseTransform]):
        self.trajectory = trajectory

    def to_dict(self):
        return [pt.to_dict() for pt in self.trajectory]
#
# Responses
#


class CalibrationNoContent(Response):
    def __init__(self, id: int, external_id: str, created: datetime):
        self.id = id
        self.external_id = external_id
        self.created = created

    @staticmethod
    def from_json(js: dict):
        return CalibrationNoContent(
            int(js["id"]), js["externalId"], ts_to_dt(js["created"])
        )

    def __repr__(self):
        return f"<CalibrationNoContent(" + \
            f"id={self.id}, " + \
            f"external_id={self.external_id}, " + \
            f"created={self.created})>"


class CalibrationWithContent(Response):
    def __init__(self, id: int, external_id: str, created: datetime,
                 calibration: Mapping[str, dict]):
        self.id = id
        self.external_id = external_id
        self.created = created
        self.calibration = calibration

    @staticmethod
    def from_json(js: dict):
        return CalibrationWithContent(int(js["id"]), js["externalId"],
                                      ts_to_dt(js["created"]), js["calibration"])

    def __repr__(self):
        return f"<CalibrationWithContent(" + \
            f"id={self.id}, " + \
            f"external_id={self.external_id}, " + \
            f"created={self.created}, " + \
            f"calibration={{...}})>"


class InputList(Response):
    def __init__(self, id: int, project_id: int, name: str, created: datetime):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.created = created

    @staticmethod
    def from_json(js: dict):
        return InputList(int(js["id"]), int(js["projectId"]), js["name"],
                         ts_to_dt(js["created"]))

    def __repr__(self):
        return f"<InputList(" + \
            f"id={self.id}, " + \
            f"project_id={self.project_id}, " + \
            f"name={self.name}, " + \
            f"created={self.created})>"


class InputBatch(Response):
    def __init__(self, external_id: str, title: str, status: InputBatchStatus,
                 created: datetime, updated: datetime):
        self.external_id = external_id
        self.title = title
        self.status = status
        self.created = created
        self.updated = updated

    @staticmethod
    def from_json(js: dict):
        return InputBatch(js["externalId"], js["title"], js["status"],
                          ts_to_dt(js["created"]), ts_to_dt(js["updated"]))

    def __repr__(self):
        return f"<InputBatch(" + \
            f"external_id={self.external_id}, " + \
            f"title={self.title}, " + \
            f"status={self.status}, " + \
            f"created={self.created}, " + \
            f"updated={self.updated})>"


class Project(Response):
    def __init__(self, created: datetime, title: str, description: str,
                 status: str, external_id: str):
        self.created = created
        self.title = title
        self.description = description
        self.status = status
        self.external_id = external_id

    @staticmethod
    def from_json(js: dict):
        return Project(ts_to_dt(js["created"]), js["title"],
                       js["description"], js["status"], js["externalId"])

    def __repr__(self):
        return f"<Project(" + \
            f"created={self.created}, " + \
            f"title={self.title}, " + \
            f"description={self.description}, " + \
            f"status={self.status}, " + \
            f"external_id={self.external_id})>"


class Request(Response):
    def __init__(self, id: int, created: datetime, project_id: int, title: str, description: str,
                 input_list_id: int, input_batch_id: int, external_id: str):
        self.id = id
        self.created = created
        self.project_id = project_id
        self.title = title
        self.description = description
        self.input_list_id = input_list_id
        self.input_batch_id = input_batch_id
        self.external_id = external_id

    @staticmethod
    def from_json(js: dict):
        return Request(int(js["id"]), ts_to_dt(js["created"]), int(js["projectId"]),
                       js["title"], js["description"], int(js["inputListId"]),
                       int(js["inputBatchId"]), js["externalId"])

    def __repr__(self):
        return f"<Request(" + \
            f"id={self.id}, " + \
            f"created={self.created}, " + \
            f"project_id={self.project_id}, " + \
            f"title={self.title}, " + \
            f"description={self.description}, " + \
            f"input_list_id={self.input_list_id}, " + \
            f"input_batch_id={self.input_batch_id}, " + \
            f"external_id={self.external_id})>"


class ExportAnnotation(Response):
    def __init__(self, annotation_id: int, export_content: dict):
        self.annotation_id = annotation_id
        self.export_content = export_content

    @staticmethod
    def from_json(js: dict):
        return ExportAnnotation(int(js["annotationId"]), js["exportContent"])

    def __repr__(self):
        return f"<ExportAnnotation(" + \
            f"annotation_id={self.annotation_id}, " + \
            f"export_content={{...}})>"


class InputJob(Response):
    def __init__(self, id: int, internal_id: str, external_id: str, filename: str,
                 status: str, added: datetime, error_message: Optional[str]):
        self.id = id
        self.internal_id = internal_id
        self.external_id = external_id
        self.filename = filename
        self.status = status
        self.added = added
        self.error_message = error_message

    @staticmethod
    def from_json(js: dict):
        return InputJob(int(js["id"]), js["jobId"], js["externalId"], js["filename"],
                        str(js["status"]), ts_to_dt(js["added"]), js.get("errorMessage"))

    def __repr__(self):
        return f"<InputJob(" + \
            f"id={self.id}, " + \
            f"internal_id={self.internal_id}, " + \
            f"external_id={self.external_id}, " + \
            f"filename={self.filename}, " + \
            f"status={self.status}, " + \
            f"added={self.added}, " + \
            f"error_message={self.error_message})>"


class CreateInputJobResponse(Response):
    def __init__(self, internal_id: int):
        self.internal_id = internal_id

    @staticmethod
    def from_json(js: dict):
        return CreateInputJobResponse(js["internalId"])

    def __repr__(self):
        return f"<CreateInputJobResponse(" + \
               f"internal_id={self.internal_id})>"


class Data(Response):
    def __init__(self, id, external_id: str, source: Optional[str], created: datetime):
        self.id = id
        self.external_id = external_id
        self.source = source
        self.created = created

    @staticmethod
    def from_json(js: dict):
        return Data(
            int(js["id"]),
            str(js.get("externalId")),
            js.get("source"),
            ts_to_dt(js["created"])
        )

    def __repr__(self):
        return f"<Data(" + \
            f"id={self.id}, " + \
            f"external_id={self.external_id}, " + \
            f"source={self.source}, " + \
            f"created={self.created})>"


class Input(Response):
    def __init__(
        self,
        internal_id: str,
        external_id: str,
        batch: str,
        input_type: str,
        status: InputStatus,
        error_message: Optional[str],
    ):
        self.internal_id = internal_id
        self.external_id = external_id
        self.batch = batch
        self.input_type = input_type
        self.status = status
        self.error_message = error_message

    @staticmethod
    def from_json(js: dict):
        return Input(
            js["internalId"],
            js["externalId"],
            js["batchId"],
            js["inputType"],
            js.get("status"),
            js.get("errorMessage")
        )

    def __repr__(self):
        return f"<Input(" + \
            f"internal_id={self.internal_id}, " + \
            f"external_id={self.external_id}, " + \
            f"input_type={self.input_type}, " + \
            f"batch={self.batch}, " + \
            f"status={self.status})>"


class InvalidatedInputsResponse(Response):
    def __init__(self, invalidated_input_ids: List[int], not_found_input_ids: List[int],
                 already_invalidated_input_ids: List[int]):
        self.invalidated_input_ids = invalidated_input_ids
        self.not_found_input_ids = not_found_input_ids
        self.already_invalidated_input_ids = already_invalidated_input_ids

    @staticmethod
    def from_json(js: dict):
        return InvalidatedInputsResponse(js["invalidatedInputIds"],
                                         js["notFoundInputIds"],
                                         js["alreadyInvalidatedInputIds"])

    def __repr__(self):
        return f"<InvalidatedInputsResponse(" + \
               f"invalidated_input_ids={self.invalidated_input_ids}, " + \
               f"not_found_input_ids={self.not_found_input_ids}, " + \
               f"already_invalidated_input_ids={self.already_invalidated_input_ids})>"


class RemovedInputsResponse(Response):
    def __init__(self, removed_input_ids: List[int], not_found_input_ids: List[int],
                 already_removed_input_ids: List[int]):
        self.removed_input_ids = removed_input_ids
        self.not_found_input_ids = not_found_input_ids
        self.already_removed_input_ids = already_removed_input_ids

    @staticmethod
    def from_json(js: dict):
        return InvalidatedInputsResponse(js["removedInputIds"],
                                         js["notFoundInputIds"],
                                         js["alreadyRemovedInputIds"])

    def __repr__(self):
        return f"<RemovedInputsResponse(" + \
               f"removed_input_ids={self.removed_input_ids}, " + \
               f"not_found_input_ids={self.not_found_input_ids}, " + \
               f"already_removed_input_ids={self.already_removed_input_ids})>"


class UploadUrlsResponse(Response):
    def __init__(self, files_to_url: Dict[str, str], internal_id: int):
        self.files_to_url = files_to_url
        self.internal_id = internal_id

    @staticmethod
    def from_json(js: dict):
        return UploadUrlsResponse(js["files"], js["jobId"])

    def __repr__(self):
        return f"<UploadUrlsResponse(" + \
               f"files_to_url={self.files_to_url}, " + \
               f"internal_id={self.internal_id})>"
