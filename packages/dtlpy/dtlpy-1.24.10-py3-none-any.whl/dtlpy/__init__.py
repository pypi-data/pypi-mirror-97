#! /usr/bin/env python3
# This file is part of DTLPY.
#
# DTLPY is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DTLPY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DTLPY.  If not, see <http://www.gnu.org/licenses/>.
import logging
import sys
import os

from .services import DataloopLogger, ApiClient, check_sdk, Reporter, VerboseLoggingLevel
from .exceptions import PlatformException
from . import repositories, exceptions, entities, examples
from .__version__ import version as __version__
from .entities import (
    Box,
    Cube,
    Point,
    Note,
    Segmentation,
    GitCodebase,
    ItemCodebase,
    FilesystemCodebase,
    PackageCodebaseType,
    OntologySpec,
    Polygon,
    Project, MemberRole,
    Dataset,
    Ellipse,
    Classification,
    Subtitle,
    Polyline,
    Pose,
    Description,
    Filters,
    Webhook, HttpMethod,
    Trigger,
    AnnotationCollection,
    Annotation, ViewAnnotationOptions, AnnotationStatus, AnnotationType,
    Item, ItemStatus,
    Codebase,
    Execution, ExecutionStatus,
    Recipe,
    Ontology,
    Label,
    Similarity, SimilarityTypeEnum,
    MultiView,
    ItemLink, UrlLink, LinkTypeEnum,
    KubernetesAutuscalerType, KubernetesRabbitmqAutoscaler, KubernetesAutoscaler, KubernetesRuntime, InstanceCatalog,
    PackageModule,
    PackageFunction,
    FunctionIO,
    Modality, ModalityTypeEnum, ModalityRefTypeEnum,
    Model, ModelOutputType, ModelInputType,
    Snapshot, SnapshotPartitionType,
    BucketType, Bucket, ItemBucket, GCSBucket, LocalBucket,
    BaseModelAdapter,
    Workload, WorkloadUnit,
    FiltersKnownFields, FiltersResource, FiltersOperations, FiltersMethod, FiltersOrderByDirection,
    FiltersKnownFields as KnownFields,
    TriggerResource, TriggerAction, TriggerExecutionMode, TriggerType,
    PackageInputType, FunctionPostAction, FunctionPostActionType, FunctionDisplayScope, FunctionDisplayScopeResource,
    Service, Package
)
from .utilities import Converter, BaseServiceRunner, Progress, AnnotationFormat
from .repositories.packages import PackageCatalog
from .repositories import FUNCTION_END_LINE

# check python version
if sys.version_info.major != 3:
    if sys.version_info.minor not in [5, 6]:
        sys.stderr.write(
            'Error: Your Python version "{}.{}" is NOT supported by Dataloop SDK dtlpy. '
            "Supported version are 3.5, 3.6)\n".format(
                sys.version_info.major, sys.version_info.minor
            )
        )
        sys.exit(-1)

if os.name == "nt":
    # set encoding for windows printing
    os.environ["PYTHONIOENCODING"] = ":replace"

"""
Main Platform Interface module for Dataloop
"""
##########
# Logger #
##########
logger = logging.getLogger(name=__name__)
if len(logger.handlers) == 0:
    logger.setLevel(logging.DEBUG)
    log_filepath = DataloopLogger.get_log_filepath()
    # set file handler to save all logs to file
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d [%(levelname)s]-[%(threadName)s]-[v" + __version__ + "]%(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = DataloopLogger(log_filepath, maxBytes=(1048 * 1000 * 5))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    # set handlers to main logger
    logger.addHandler(sh)
    logger.addHandler(fh)

################
# Repositories #
################
# Create repositories instances
client_api = ApiClient()
projects = repositories.Projects(client_api=client_api)
datasets = repositories.Datasets(client_api=client_api, project=None)
items = repositories.Items(client_api=client_api, datasets=datasets)
packages = repositories.Packages(client_api=client_api)
executions = repositories.Executions(client_api=client_api)
services = repositories.Services(client_api=client_api)
webhooks = repositories.Webhooks(client_api=client_api)
triggers = repositories.Triggers(client_api=client_api)
assignments = repositories.Assignments(client_api=client_api)
tasks = repositories.Tasks(client_api=client_api)
annotations = repositories.Annotations(client_api=client_api)
models = repositories.Models(client_api=client_api)
snapshots = repositories.Snapshots(client_api=client_api)
buckets = repositories.Buckets(client_api=client_api)
ontologies = repositories.Ontologies(client_api=client_api)

try:
    check_sdk.check(version=__version__, client_api=client_api)
except Exception:
    logger.debug("Failed to check SDK! Continue without")

verbose = client_api.verbose
login = client_api.login
login_token = client_api.login_token
login_secret = client_api.login_secret
login_m2m = client_api.login_m2m
add_environment = client_api.add_environment
setenv = client_api.setenv
token_expired = client_api.token_expired
info = client_api.info


def token():
    """
    token
    :return: token in use
    """
    return client_api.token


def environment():
    """
    environment
    :return: current environment
    """
    return client_api.environment


def init():
    """
    init current directory as a Dataloop working directory
    :return:
    """
    from .services import CookieIO

    client_api.state_io = CookieIO.init_local_cookie(create=True)
    assert isinstance(client_api.state_io, CookieIO)
    logger.info(".Dataloop directory initiated successfully in {}".format(os.getcwd()))


def checkout_state():
    """
    Return the current checked out state
    :return:
    """
    state = client_api.state_io.read_json()
    return state


class LoggingLevel:
    DEBUG = "debug"
    WARNING = "warning"
    CRITICAL = "critical"
    INFO = "info"


#################
#     ENUMS     #
#################
LOGGING_LEVEL_DEBUG = LoggingLevel.DEBUG
LOGGING_LEVEL_WARNING = LoggingLevel.WARNING
LOGGING_LEVEL_CRITICAL = LoggingLevel.CRITICAL
LOGGING_LEVEL_INFO = LoggingLevel.INFO

VERBOSE_LOGGING_LEVEL_DEBUG = VerboseLoggingLevel.DEBUG
VERBOSE_LOGGING_LEVEL_INFO = VerboseLoggingLevel.INFO
VERBOSE_LOGGING_LEVEL_WARNING = VerboseLoggingLevel.WARNING
VERBOSE_LOGGING_LEVEL_ERROR = VerboseLoggingLevel.ERROR
VERBOSE_LOGGING_LEVEL_CRITICAL = VerboseLoggingLevel.CRITICAL

HTTP_METHOD_POST = HttpMethod.POST
HTTP_METHOD_GET = HttpMethod.GET
HTTP_METHOD_DELETE = HttpMethod.DELETE
HTTP_METHOD_PATCH = HttpMethod.PATCH

VIEW_ANNOTATION_OPTIONS_JSON = ViewAnnotationOptions.JSON
VIEW_ANNOTATION_OPTIONS_MASK = ViewAnnotationOptions.MASK
VIEW_ANNOTATION_OPTIONS_ANNOTATION_ON_IMAGE = ViewAnnotationOptions.ANNOTATION_ON_IMAGE
VIEW_ANNOTATION_OPTIONS_INSTANCE = ViewAnnotationOptions.INSTANCE
VIEW_ANNOTATION_OPTIONS_VTT = ViewAnnotationOptions.VTT
VIEW_ANNOTATION_OPTIONS_OBJECT_ID = ViewAnnotationOptions.OBJECT_ID

ANNOTATION_STATUS_ISSUE = AnnotationStatus.ISSUE
ANNOTATION_STATUS_REVIEW = AnnotationStatus.REVIEW
ANNOTATION_STATUS_APPROVED = AnnotationStatus.APPROVED
ANNOTATION_STATUS_CLEAR = AnnotationStatus.CLEAR

# class
ANNOTATION_TYPE_BOX = AnnotationType.BOX
ANNOTATION_TYPE_CLASSIFICATION = AnnotationType.CLASSIFICATION
ANNOTATION_TYPE_COMPARISON = AnnotationType.COMPARISON
ANNOTATION_TYPE_ELLIPSE = AnnotationType.ELLIPSE
ANNOTATION_TYPE_NOTE = AnnotationType.NOTE
ANNOTATION_TYPE_POINT = AnnotationType.POINT
ANNOTATION_TYPE_POLYGON = AnnotationType.POLYGON
ANNOTATION_TYPE_POLYLINE = AnnotationType.POLYLINE
ANNOTATION_TYPE_POSE = AnnotationType.POSE
ANNOTATION_TYPE_SEGMENTATION = AnnotationType.SEGMENTATION
ANNOTATION_TYPE_SUBTITLE = AnnotationType.SUBTITLE

ITEM_STATUS_COMPLETED = ItemStatus.COMPLETED
ITEM_STATUS_APPROVED = ItemStatus.APPROVED
ITEM_STATUS_DISCARDED = ItemStatus.DISCARDED

EXECUTION_STATUS_CREATED = ExecutionStatus.CREATED
EXECUTION_STATUS_IN_PROGRESS = ExecutionStatus.IN_PROGRESS
EXECUTION_STATUS_SUCCESS = ExecutionStatus.SUCCESS
EXECUTION_STATUS_FAILED = ExecutionStatus.FAILED

SIMILARITY_TYPE_ID = SimilarityTypeEnum.ID
SIMILARITY_TYPE_URL = SimilarityTypeEnum.URL

LINK_TYPE_ID = LinkTypeEnum.ID
LINK_TYPE_URL = LinkTypeEnum.URL

KUBERNETES_AUTUSCALER_TYPE_CPU = KubernetesAutuscalerType.CPU
KUBERNETES_AUTUSCALER_TYPE_RABBITMQ = KubernetesAutuscalerType.RABBITMQ

INSTANCE_CATALOG_REGULAR_XS = InstanceCatalog.REGULAR_XS
INSTANCE_CATALOG_REGULAR_S = InstanceCatalog.REGULAR_S
INSTANCE_CATALOG_REGULAR_M = InstanceCatalog.REGULAR_M
INSTANCE_CATALOG_REGULAR_L = InstanceCatalog.REGULAR_L
INSTANCE_CATALOG_REGULAR_XL = InstanceCatalog.REGULAR_XL
INSTANCE_CATALOG_HIGHMEM_XS = InstanceCatalog.HIGHMEM_XS
INSTANCE_CATALOG_HIGHMEM_S = InstanceCatalog.HIGHMEM_S
INSTANCE_CATALOG_HIGHMEM_M = InstanceCatalog.HIGHMEM_M
INSTANCE_CATALOG_HIGHMEM_L = InstanceCatalog.HIGHMEM_L
INSTANCE_CATALOG_HIGHMEM_XL = InstanceCatalog.HIGHMEM_XL
INSTANCE_CATALOG_GPU_K80_S = InstanceCatalog.GPU_K80_S
INSTANCE_CATALOG_GPU_K80_M = InstanceCatalog.GPU_K80_M

MODALITY_TYPE_OVERLAY = ModalityTypeEnum.OVERLAY

MODALITY_REF_TYPE_ID = ModalityRefTypeEnum.ID
MODALITY_REF_TYPE_URL = ModalityRefTypeEnum.URL

FILTERS_KNOWN_FIELDS_DIR = FiltersKnownFields.DIR
FILTERS_KNOWN_FIELDS_ANNOTATED = FiltersKnownFields.ANNOTATED
FILTERS_KNOWN_FIELDS_FILENAME = FiltersKnownFields.FILENAME
FILTERS_KNOWN_FIELDS_CREATED_AT = FiltersKnownFields.CREATED_AT
FILTERS_KNOWN_FIELDS_UPDATED_AT = FiltersKnownFields.UPDATED_AT
FILTERS_KNOWN_FIELDS_LABEL = FiltersKnownFields.LABEL
FILTERS_KNOWN_FIELDS_NAME = FiltersKnownFields.NAME
FILTERS_KNOWN_FIELDS_HIDDEN = FiltersKnownFields.HIDDEN
FILTERS_KNOWN_FIELDS_TYPE = FiltersKnownFields.TYPE

FILTERS_RESOURCE_ITEM = FiltersResource.ITEM
FILTERS_RESOURCE_ANNOTATION = FiltersResource.ANNOTATION
FILTERS_RESOURCE_EXECUTION = FiltersResource.EXECUTION
FILTERS_RESOURCE_PACKAGE = FiltersResource.PACKAGE
FILTERS_RESOURCE_SERVICE = FiltersResource.SERVICE
FILTERS_RESOURCE_TRIGGER = FiltersResource.TRIGGER
FILTERS_RESOURCE_MODEL = FiltersResource.MODEL
FILTERS_RESOURCE_SNAPSHOT = FiltersResource.SNAPSHOT
FILTERS_RESOURCE_WEBHOOK = FiltersResource.WEBHOOK
FILTERS_RESOURCE_RECIPE = FiltersResource.RECIPE
FILTERS_RESOURCE_DATASET = FiltersResource.DATASET
FILTERS_RESOURCE_ONTOLOGY = FiltersResource.ONTOLOGY

FILTERS_OPERATIONS_OR = FiltersOperations.OR
FILTERS_OPERATIONS_AND = FiltersOperations.AND
FILTERS_OPERATIONS_IN = FiltersOperations.IN
FILTERS_OPERATIONS_NOT_EQUAL = FiltersOperations.NOT_EQUAL
FILTERS_OPERATIONS_EQUAL = FiltersOperations.EQUAL
FILTERS_OPERATIONS_GREATER_THAN = FiltersOperations.GREATER_THAN
FILTERS_OPERATIONS_LESS_THAN = FiltersOperations.LESS_THAN

FILTERS_METHOD_OR = FiltersMethod.OR
FILTERS_METHOD_AND = FiltersMethod.AND

FILTERS_ORDERBY_DIRECTION_DESCENDING = FiltersOrderByDirection.DESCENDING
FILTERS_ORDERBY_DIRECTION_ASCENDING = FiltersOrderByDirection.DESCENDING

TRIGGER_RESOURCE_ITEM = TriggerResource.ITEM
TRIGGER_RESOURCE_DATASET = TriggerResource.DATASET
TRIGGER_RESOURCE_ANNOTATION = TriggerResource.ANNOTATION
TRIGGER_RESOURCE_ITEM_STATUS = TriggerResource.ITEM_STATUS

TRIGGER_ACTION_CREATED = TriggerAction.CREATED
TRIGGER_ACTION_UPDATED = TriggerAction.UPDATED
TRIGGER_ACTION_DELETED = TriggerAction.DELETED

TRIGGER_EXECUTION_MODE_ONCE = TriggerExecutionMode.ONCE
TRIGGER_EXECUTION_MODE_ALWAYS = TriggerExecutionMode.ALWAYS

TRIGGER_TYPE_EVENT = TriggerType.EVENT
TRIGGER_TYPE_CRON = TriggerType.CRON

PACKAGE_INPUT_TYPE_ITEM = PackageInputType.ITEM
PACKAGE_INPUT_TYPE_DATASET = PackageInputType.DATASET
PACKAGE_INPUT_TYPE_ANNOTATION = PackageInputType.ANNOTATION
PACKAGE_INPUT_TYPE_JSON = PackageInputType.JSON
PACKAGE_INPUT_TYPE_MODEL = PackageInputType.MODEL
PACKAGE_INPUT_TYPE_SNAPSHOT = PackageInputType.SNAPSHOT
PACKAGE_INPUT_TYPE_PACKAGE = PackageInputType.PACKAGE
PACKAGE_INPUT_TYPE_SERVICE = PackageInputType.SERVICE
PACKAGE_INPUT_TYPE_PROJECT = PackageInputType.PROJECT
PACKAGE_INPUT_TYPE_EXECUTION = PackageInputType.EXECUTION

FUNCTION_POST_ACTION_TYPE_DOWNLOAD = FunctionPostActionType.DOWNLOAD
FUNCTION_POST_ACTION_TYPE_DRAW_ANNOTATION = FunctionPostActionType.DRAW_ANNOTATION
FUNCTION_POST_ACTION_TYPE_NO_ACTION = FunctionPostActionType.NO_ACTION

FUNCTION_DISPLAY_SCOPE_RESOURCE_ANNOTATION = FunctionDisplayScopeResource.ANNOTATION
FUNCTION_DISPLAY_SCOPE_RESOURCE_ITEM = FunctionDisplayScopeResource.ITEM
FUNCTION_DISPLAY_SCOPE_RESOURCE_DATASET = FunctionDisplayScopeResource.DATASET
FUNCTION_DISPLAY_SCOPE_RESOURCE_DATASET_QUERY = FunctionDisplayScopeResource.DATASET_QUERY

MEMBER_ROLE_OWNER = MemberRole.OWNER
MEMBER_ROLE_DEVELOPER = MemberRole.DEVELOPER
MEMBER_ROLE_ANNOTATOR = MemberRole.ANNOTATOR
MEMBER_ROLE_ANNOTATION_MANAGER = MemberRole.ANNOTATION_MANAGER
