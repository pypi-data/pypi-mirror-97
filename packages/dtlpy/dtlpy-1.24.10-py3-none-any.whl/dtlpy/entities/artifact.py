import traceback
import logging
import attr
import copy

from .. import entities

logger = logging.getLogger(name=__name__)


@attr.s
class Artifact(entities.Item):

    @staticmethod
    def _protected_from_json(_json, client_api, dataset=None, project=None, is_fetched=True):
        """
        Same as from_json but with try-except to catch if error
        :param _json:
        :param client_api:
        :param dataset:
        :return:
        """
        try:
            artifact = Artifact.from_json(_json=_json,
                                          client_api=client_api,
                                          dataset=dataset,
                                          project=None,
                                          is_fetched=True)
            status = True
        except Exception:
            artifact = traceback.format_exc()
            status = False
        return status, artifact

    @classmethod
    def from_json(cls, _json, client_api, dataset=None, project=None, is_fetched=True):
        """
        Build an Artifact entity object from a json
        :param project:
        :param _json: _json response from host
        :param dataset: Artifact's dataset
        :param client_api: client_api
        :param is_fetched: is Entity fetched from Platform
        :return: Artifact object
        """

        inst = cls(
            # sdk
            platform_dict=copy.deepcopy(_json),
            client_api=client_api,
            dataset=dataset,
            project=project,
            # params
            annotations_link=_json.get('annotations_link', None),
            annotations_count=_json.get('annotationsCount', None),
            createdAt=_json.get('createdAt', None),
            datasetId=_json.get('datasetId', None),
            thumbnail=_json.get('thumbnail', None),
            annotated=_json.get('annotated', None),
            dataset_url=_json.get('dataset', None),
            filename=_json.get('filename', None),
            metadata=_json.get('metadata', None),
            hidden=_json.get('hidden', False),
            stream=_json.get('stream', None),
            name=_json.get('name', None),
            type=_json.get('type', None),
            dir=_json.get('dir', None),
            url=_json.get('url', None),
            id=_json['id'])
        inst.is_fetched = is_fetched
        return inst
