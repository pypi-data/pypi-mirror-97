import traceback
import logging
import attr

from .. import entities, exceptions, repositories

logger = logging.getLogger(name=__name__)


@attr.s
class Bot(entities.User):
    """
    Bot entity
    """
    _bots = attr.ib(repr=False, default=None)

    @staticmethod
    def _protected_from_json(_json, project, client_api, bots=None):
        """
        Same as from_json but with try-except to catch if error
        :param _json:
        :param project:
        :return:
        """
        try:
            bot = Bot.from_json(_json=_json,
                                project=project,
                                bots=bots,
                                client_api=client_api)
            status = True
        except Exception:
            bot = traceback.format_exc()
            status = False
        return status, bot

    @classmethod
    def from_json(cls, _json, project, client_api, bots=None):
        """
        Build a Bot entity object from a json

        :param client_api:
        :param _json: _json response from host
        :param project: project entity
        :param bots: Bots repository
        :return: User object
        """
        return cls(
            createdAt=_json.get('createdAt', None),
            name=_json.get('firstName', None),
            updatedAt=_json.get('updatedAt', None),
            last_name=_json.get('lastName', None),
            username=_json.get('username', None),
            avatar=_json.get('avatar', None),
            email=_json.get('email', None),
            type=_json.get('type', None),
            role=_json.get('role', None),
            org=_json.get('org', None),
            id=_json.get('id', None),
            project=project,
            client_api=client_api,
            bots=bots
        )

    @property
    def bots(self):
        if self._bots is None:
            self._bots = repositories.Bots(client_api=self._client_api, project=self._project)
        assert isinstance(self._bots, repositories.Bots)
        return self._bots

    @property
    def project(self):
        if self._project is None:
            raise exceptions.PlatformException(error='2001',
                                               message='Missing entity "project".')
        assert isinstance(self._project, entities.Project)
        return self._project

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        """
        _json = attr.asdict(self,
                            filter=attr.filters.exclude(attr.fields(Bot)._project,
                                                        attr.fields(Bot).name,
                                                        attr.fields(Bot)._client_api,
                                                        attr.fields(Bot)._bots,
                                                        attr.fields(Bot)._users,
                                                        attr.fields(Bot).last_name))
        _json['firstName'] = self.name
        _json['lastName'] = self.last_name
        return _json

    def delete(self):
        """
        Delete the bot

        :return: True
        """
        return self.bots.delete(bot_id=self.id)
