import traceback
from collections import namedtuple
import logging
import attr

from .. import repositories, entities, services, exceptions

logger = logging.getLogger(name=__name__)


@attr.s
class Recipe(entities.BaseEntity):
    """
    Recipe object
    """
    id = attr.ib()
    creator = attr.ib()
    url = attr.ib(repr=False)
    title = attr.ib()
    project_ids = attr.ib()
    description = attr.ib()
    ontologyIds = attr.ib(repr=False)
    instructions = attr.ib(repr=False)
    examples = attr.ib(repr=False)
    customActions = attr.ib(repr=False)
    metadata = attr.ib()

    # name change
    ui_settings = attr.ib()

    # platform
    _client_api = attr.ib(type=services.ApiClient, repr=False)
    # entities
    _dataset = attr.ib(repr=False, default=None)
    _project = attr.ib(repr=False, default=None)
    # repositories
    _repositories = attr.ib(repr=False)

    @classmethod
    def from_json(cls, _json, client_api, dataset=None, project=None, is_fetched=True):
        """
        Build a Recipe entity object from a json

        :param _json: _json response from host
        :param dataset: recipe's dataset
        :param project: recipe's project
        :param client_api: client_api
        :param is_fetched: is Entity fetched from Platform
        :return: Recipe object
        """
        project_ids = _json.get('projectIds', None)
        if project is not None and project_ids is not None:
            if project.id not in project_ids:
                logger.warning('Recipe has been fetched from a project that is not belong to it')
                project = None

        inst = cls(
            client_api=client_api,
            dataset=dataset,
            project=project,
            id=_json['id'],
            creator=_json.get('creator', None),
            url=_json.get('url', None),
            title=_json.get('title', None),
            project_ids=project_ids,
            description=_json.get('description', None),
            ontologyIds=_json.get('ontologyIds', None),
            instructions=_json.get('instructions', None),
            ui_settings=_json.get('uiSettings', None),
            metadata=_json.get('metadata', None),
            examples=_json.get('examples', None),
            customActions=_json.get('customActions', None))
        inst.is_fetched = is_fetched
        return inst

    @staticmethod
    def _protected_from_json(_json, client_api, project=None, dataset=None, is_fetched=True):
        """
        Same as from_json but with try-except to catch if error
        :param _json:
        :param client_api:
        :param dataset:
        :return:
        """
        try:
            recipe = Recipe.from_json(_json=_json,
                                      client_api=client_api,
                                      project=project,
                                      dataset=dataset,
                                      is_fetched=is_fetched)
            status = True
        except Exception:
            recipe = traceback.format_exc()
            status = False
        return status, recipe

    @_repositories.default
    def set_repositories(self):
        reps = namedtuple('repositories',
                          field_names=['ontologies', 'recipes'])
        if self._dataset is None and self._project is None:
            recipes = repositories.Recipes(client_api=self._client_api, dataset=self._dataset, project=self._project)
        elif self._dataset is not None:
            recipes = self.dataset.recipes
        else:
            recipes = self.project.recipes
        r = reps(ontologies=repositories.Ontologies(recipe=self, client_api=self._client_api),
                 recipes=recipes)
        return r

    @property
    def dataset(self):
        if self._dataset is not None:
            assert isinstance(self._dataset, entities.Dataset)
        return self._dataset

    @property
    def project(self):
        if self._project is not None:
            assert isinstance(self._project, entities.Project)
        return self._project

    @property
    def recipes(self):
        assert isinstance(self._repositories.recipes, repositories.Recipes)
        return self._repositories.recipes

    @property
    def ontologies(self):
        assert isinstance(self._repositories.ontologies, repositories.Ontologies)
        return self._repositories.ontologies

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        """
        _json = attr.asdict(self, filter=attr.filters.exclude(attr.fields(Recipe)._client_api,
                                                              attr.fields(Recipe)._dataset,
                                                              attr.fields(Recipe)._project,
                                                              attr.fields(Recipe).project_ids,
                                                              attr.fields(Recipe).ui_settings,
                                                              attr.fields(Recipe)._repositories))
        _json['uiSettings'] = self.ui_settings
        _json['projectIds'] = self.project_ids
        return _json

    def delete(self):
        """
        Delete recipe from platform

        :return: True
        """
        return self.recipes.delete(self.id)

    def update(self, system_metadata=False):
        """
        Update Recipe

        :param system_metadata: bool
        :return: Recipe object
        """
        return self.recipes.update(recipe=self, system_metadata=system_metadata)

    def clone(self, shallow=False):
        """
        Clone Recipe

       :param shallow: If True, link ot existing ontology, clones all ontology that are link to the recipe as well
       :return: Cloned ontology object
        """
        return self.recipes.clone(recipe=self,
                                  shallow=shallow)

    def get_annotation_template_id(self, template_name):
        """
        Get annotation template id by template name

       :param template_name:
       :return: template id or None if does not exist
        """
        collection_templates = list()
        if 'system' in self.metadata and 'collectionTemplates' in self.metadata['system']:
            collection_templates = self.metadata['system']['collectionTemplates']

        for template in collection_templates:
            if "name" and 'id' in template:
                if template_name == template['name']:
                    return template['id']
        raise exceptions.NotFound('404', "annotation template {!r} not found".format(template_name))
