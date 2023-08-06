import importlib.util
import inspect
import logging
import json
import os
from copy import deepcopy
from shutil import copyfile
from multiprocessing.pool import ThreadPool
from typing import Union, List

from .. import entities, repositories, exceptions, utilities, miscellaneous, assets, services

logger = logging.getLogger(name=__name__)

DEFAULT_PACKAGE_METHOD = entities.PackageFunction(name=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME,
                                                  description='',
                                                  inputs=[],
                                                  outputs=[])
DEFAULT_PACKAGE_MODULE = entities.PackageModule(init_inputs=list(),
                                                entry_point=entities.package_defaults.DEFAULT_PACKAGE_ENTRY_POINT,
                                                class_name=entities.package_defaults.DEFAULT_PACKAGE_CLASS_NAME,
                                                name=entities.package_defaults.DEFAULT_PACKAGE_MODULE_NAME,
                                                functions=[DEFAULT_PACKAGE_METHOD])


class PackageCatalog:
    DEFAULT_PACKAGE_TYPE = 'default_package_type'
    MULTI_MODULE = 'multi_module'
    MULTI_MODULE_WITH_TRIGGER = 'multi_module_with_trigger'
    SINGLE_FUNCTION_ITEM = 'single_function_item'
    SINGLE_FUNCTION_JSON = 'single_function_json'
    SINGLE_FUNCTION_DATASET = 'single_function_dataset'
    SINGLE_FUNCTION_ANNOTATION = 'single_function_annotation'
    SINGLE_FUNCTION_NO_INPUT = 'single_function_no_input'
    SINGLE_FUNCTION_MULTI_INPUT = 'single_function_multi_input'
    MULTI_FUNCTION_ITEM = 'multi_function_item'
    MULTI_FUNCTION_DATASET = 'multi_function_dataset'
    MULTI_FUNCTION_ANNOTATION = 'multi_function_annotation'
    MULTI_FUNCTION_NO_INPUT = 'multi_function_no_input'
    MULTI_FUNCTION_JSON = 'multi_function_json'
    SINGLE_FUNCTION_ITEM_WITH_TRIGGER = 'single_function_item_with_trigger'
    SINGLE_FUNCTION_DATASET_WITH_TRIGGER = 'single_function_dataset_with_trigger'
    SINGLE_FUNCTION_ANNOTATION_WITH_TRIGGER = 'single_function_annotation_with_trigger'
    MULTI_FUNCTION_ITEM_WITH_TRIGGERS = 'multi_function_item_with_triggers'
    MULTI_FUNCTION_DATASET_WITH_TRIGGERS = 'multi_function_dataset_with_triggers'
    MULTI_FUNCTION_ANNOTATION_WITH_TRIGGERS = 'multi_function_annotation_with_triggers'
    CONVERTER_FUNCTION = 'converter'


class Packages:
    """
    Packages Repository
    """

    def __init__(self, client_api: services.ApiClient, project: entities.Project = None):
        self._client_api = client_api
        self._project = project
        self.package_io = PackageIO()

    ############
    # entities #
    ############
    @property
    def project(self) -> entities.Project:
        if self._project is None:
            try:
                self._project = repositories.Projects(client_api=self._client_api).get()
            except exceptions.NotFound:
                raise exceptions.PlatformException(
                    error='2001',
                    message='Missing "project". need to set a Project entity or use project.packages repository')
        return self._project

    @project.setter
    def project(self, project: entities.Project):
        if not isinstance(project, entities.Project):
            raise ValueError('Must input a valid Project entity')
        self._project = project

    ###########
    # methods #
    ###########
    def open_in_web(self, package=None, package_id=None, package_name=None):
        if package is None:
            package = self.get(package_name=package_name, package_id=package_id)
        self._client_api._open_in_web(resource_type='package', project_id=package.project_id, package_id=package.id)

    def revisions(self, package: entities.Package = None, package_id=None):
        """
        Get package revisions history

        :param package: Package entity
        :param package_id: package id
        """
        if package is None and package_id is None:
            raise exceptions.PlatformException(
                error='400',
                message='must provide an identifier in inputs: "package" or "package_id"')
        if package is not None:
            package_id = package.id

        success, response = self._client_api.gen_request(
            req_type="get",
            path="/packages/{}/revisions".format(package_id))
        if not success:
            raise exceptions.PlatformException(response)
        return response.json()

    def get(self, package_name=None, package_id=None, checkout=False, fetch=None) -> entities.Package:
        """
        Get Package object

        :param checkout:
        :param package_id:
        :param package_name:
        :param fetch: optional - fetch entity from platform, default taken from cookie
        :return: Package object
        """
        if fetch is None:
            fetch = self._client_api.fetch_entities

        if package_name is None and package_id is None:
            package = self.__get_from_cache()
            if package is None:
                raise exceptions.PlatformException(
                    error='400',
                    message='No checked-out Package was found, must checkout or provide an identifier in inputs')
        elif fetch:
            if package_id is not None:
                success, response = self._client_api.gen_request(
                    req_type="get",
                    path="/packages/{}".format(package_id))
                if not success:
                    raise exceptions.PlatformException(response)
                package = entities.Package.from_json(client_api=self._client_api,
                                                     _json=response.json(),
                                                     project=self._project)
                # verify input package name is same as the given id
                if package_name is not None and package.name != package_name:
                    logger.warning(
                        "Mismatch found in packages.get: package_name is different then package.name:"
                        " {!r} != {!r}".format(
                            package_name,
                            package.name))
            elif package_name is not None:
                filters = entities.Filters(field='name', values=package_name, resource=entities.FiltersResource.PACKAGE,
                                           use_defaults=False)
                if self._project is not None:
                    filters.add(field='projectId', values=self._project.id)
                packages = self.list(filters=filters)
                if packages.items_count == 0:
                    raise exceptions.PlatformException(
                        error='404',
                        message='Package not found. Name: {}'.format(package_name))
                elif packages.items_count > 1:
                    raise exceptions.PlatformException(
                        error='400',
                        message='More than one package found by the name of: {} '
                                'Please get package from a project entity'.format(package_name))
                package = packages.items[0]
            else:
                raise exceptions.PlatformException(
                    error='400',
                    message='No checked-out Package was found, must checkout or provide an identifier in inputs')
        else:
            package = entities.Package.from_json(_json={'id': package_id,
                                                        'name': package_name},
                                                 client_api=self._client_api,
                                                 project=self._project,
                                                 is_fetched=False)

        if checkout:
            self.checkout(package=package)
        return package

    def _build_entities_from_response(self, response_items) -> miscellaneous.List[entities.Package]:
        pool = self._client_api.thread_pools(pool_name='entity.create')
        jobs = [None for _ in range(len(response_items))]
        # return triggers list
        for i_package, package in enumerate(response_items):
            jobs[i_package] = pool.apply_async(entities.Package._protected_from_json,
                                               kwds={'client_api': self._client_api,
                                                     '_json': package,
                                                     'project': self._project})
        # wait for all jobs
        _ = [j.wait() for j in jobs]
        # get all results
        results = [j.get() for j in jobs]
        # log errors
        _ = [logger.warning(r[1]) for r in results if r[0] is False]
        # return good jobs
        packages = miscellaneous.List([r[1] for r in results if r[0] is True])
        return packages

    def _list(self, filters: entities.Filters):
        url = '/query/faas'

        # request
        success, response = self._client_api.gen_request(req_type='post',
                                                         path=url,
                                                         json_req=filters.prepare())
        if not success:
            raise exceptions.PlatformException(response)
        return response.json()

    def list(self, filters: entities.Filters = None, project_id=None) -> entities.PagedEntities:
        """
        List project packages
        :return:
        """
        if filters is None:
            filters = entities.Filters(resource=entities.FiltersResource.PACKAGE)

        # assert type filters
        if not isinstance(filters, entities.Filters):
            raise exceptions.PlatformException('400', 'Unknown filters type')

        if project_id is None and self._project is not None:
            project_id = self._project.id

        if project_id is not None:
            filters.add(field='projectId', values=project_id)

        paged = entities.PagedEntities(items_repository=self,
                                       filters=filters,
                                       page_offset=filters.page,
                                       page_size=filters.page_size,
                                       project_id=project_id,
                                       client_api=self._client_api)
        paged.get_page()
        return paged

    def pull(self, package: entities.Package, version=None, local_path=None, project_id=None):
        """
        :param project_id:
        :param version:
        :param package:
        :param local_path:
        :return:
        """
        if isinstance(version, int):
            logger.warning('Deprecation Warning - Package/service versions have been refactored'
                           'The version you provided has type: int, it will be converted to: 1.0.{}'
                           'Next time use a 3-level semver for package/service versions'.format(version))

        if self._project is None:
            if package is not None and package.project is not None:
                self._project = package.project
            else:
                self._project = repositories.Projects(client_api=self._client_api).get(project_id=project_id,
                                                                                       fetch=None)
        dir_version = version
        if version is None:
            dir_version = package.version

        if local_path is None:
            local_path = os.path.join(
                services.service_defaults.DATALOOP_PATH,
                "projects",
                self._project.name,
                "packages",
                package.name,
                str(dir_version))

        if version is None or version == package.version:
            codebase_id = package.codebase_id
        else:
            versions = [revision for revision in package.revisions if revision['version'] == version]
            if len(versions) <= 0:
                raise exceptions.PlatformException('404', 'Version not found: version={}'.format(version))
            elif len(versions) > 1:
                raise exceptions.PlatformException('404', 'More than one version found: version={}'.format(version))
            codebase_id = versions[0]['codebaseId']

        self._project.codebases.unpack(codebase_id=codebase_id, local_path=local_path)

        return local_path

    def _name_validation(self, name: str):
        url = '/piper-misc/naming/packages/{}'.format(name)

        # request
        success, response = self._client_api.gen_request(req_type='get',
                                                         path=url)
        if not success:
            raise exceptions.PlatformException(response)

    def push(self,
             project: entities.Project = None,
             project_id: str = None,
             package_name: str = None,
             src_path: str = None,
             codebase_id: str = None,
             codebase: Union[entities.GitCodebase, entities.ItemCodebase, entities.FilesystemCodebase] = None,
             modules: List[entities.PackageModule] = None,
             is_global: bool = None,
             checkout: bool = False,
             revision_increment: str = None,
             version: str = None,
             ignore_sanity_check: bool = False) -> entities.Package:
        """
        Push local package.
        Project will be taken in the following hierarchy:
        project(input) -> project_id(input) -> self.project(context) -> checked out

        :param codebase:
        :param ignore_sanity_check:
        :param project: optional - project entity to deploy to. default from context or checked-out
        :param project_id: optional - project id to deploy to. default from context or checked-out
        :param package_name: package name
        :param checkout: checkout package to local dir
        :param codebase_id: id of the codebase item
        :param src_path: path to package codebase
        :param modules: list of modules PackageModules of the package
        :param version: semver version f the package
        :param revision_increment: optional - str - version bumping method - major/minor/patch - default = None
        :param is_global:
        :return:
        """
        # get project
        project_to_deploy = None
        if project is not None:
            project_to_deploy = project
        elif project_id is not None:
            project_to_deploy = repositories.Projects(client_api=self._client_api).get(project_id=project_id)
        elif self._project is not None:
            project_to_deploy = self._project
        else:
            try:
                project_to_deploy = repositories.Projects(client_api=self._client_api).get()
            except Exception:
                pass

        if project_to_deploy is None:
            raise exceptions.PlatformException(
                error='400',
                message='Missing project from "packages.push" function. '
                        'Please provide project or id, use Packages from a '
                        'project.packages repository or checkout a project')

        if codebase is None and codebase_id is not None:
            codebase = entities.ItemCodebase(item_id=codebase_id,
                                             client_api=self._client_api)

        # source path
        if src_path is None:
            if codebase is None:
                src_path = os.getcwd()
                logger.warning('No src_path is given, getting package information from cwd: {}'.format(src_path))

        # get package json
        package_from_json = dict()
        if assets.paths.PACKAGE_FILENAME in os.listdir(src_path):
            with open(os.path.join(src_path, assets.paths.PACKAGE_FILENAME), 'r') as f:
                package_from_json = json.load(f)

        # get name
        if package_name is None:
            package_name = package_from_json.get('name', 'default-package')

        if modules is None and 'modules' in package_from_json:
            modules = package_from_json['modules']

        if ignore_sanity_check:
            logger.warning(
                'Pushing a package without sanity check can cause errors when trying to deploy, '
                'trigger and execute functions.\n'
                'We highly recommend to not use the ignore_sanity_check flag')
        elif codebase is None:
            modules = self._sanity_before_push(src_path=src_path, modules=modules)

        self._name_validation(name=package_name)

        # get or create codebase
        codebase_item = None
        if codebase is None:
            codebase = project_to_deploy.codebases.pack(directory=src_path, name=package_name)

        try:
            # check if exist
            filters = entities.Filters(resource=entities.FiltersResource.PACKAGE, use_defaults=False)
            filters.add(field='projectId', values=project_to_deploy.id)
            filters.add(field='name', values=package_name)
            packages = self.list(filters=filters)
            if packages.items_count > 0:
                # package exists - need to update
                package = packages.items[0]

                if codebase.type == entities.PackageCodebaseType.ITEM:
                    package._codebase_id = codebase.item_id

                if modules is not None:
                    package.modules = modules

                if is_global is not None:
                    package.is_global = is_global

                if codebase is not None:
                    package.codebase = codebase

                if version is not None:
                    package.version = version

                package = self.update(package=package, revision_increment=revision_increment)
            else:
                package = self._create(
                    project_to_deploy=project_to_deploy,
                    codebase_id=codebase_id,
                    package_name=package_name,
                    modules=modules,
                    codebase=codebase,
                    is_global=is_global,
                    version=version
                )
            if checkout:
                self.checkout(package=package)
        except Exception:
            if codebase_item is not None:
                codebase_item.delete()
            raise

        logger.info("Package name: {!r}, id: {!r} has been added to project name: {!r}, id: {!r}".format(
            package.name,
            package.id,
            package.project.name,
            package.project.id))
        return package

    def _create(self,
                project_to_deploy: entities.Project = None,
                codebase_id: str = None,
                codebase: Union[entities.GitCodebase, entities.ItemCodebase, entities.FilesystemCodebase] = None,
                is_global: bool = None,
                package_name: str = entities.package_defaults.DEFAULT_PACKAGE_NAME,
                modules: List[entities.PackageModule] = None,
                version: str = None,
                ) -> entities.Package:
        """
        Create a package in platform

        :param codebase_id: optional - package codebase
        :param codebase:
        :param package_name: optional - default: 'default package'
        :param modules: optional - PackageModules Entity
        :param version: semver version of the package
        :return: Package Entity
        """
        # if is dtlpy entity convert to dict
        if modules and isinstance(modules[0], entities.PackageModule):
            modules = [module.to_json() for module in modules]

        if is_global is None:
            is_global = False

        payload = {'name': package_name,
                   'global': is_global,
                   'modules': modules
                   }

        if codebase_id is not None:
            payload['codebaseId'] = codebase_id

        if codebase is not None:
            payload['codebase'] = codebase.to_json()

        if version is not None:
            payload['version'] = version

        if project_to_deploy is not None:
            payload['projectId'] = project_to_deploy.id
        else:
            raise exceptions.PlatformException('400', 'Repository must have a project to perform this action')

        # request
        success, response = self._client_api.gen_request(req_type='post',
                                                         path='/packages',
                                                         json_req=payload)

        # exception handling
        if not success:
            raise exceptions.PlatformException(response)

        # return entity
        return entities.Package.from_json(_json=response.json(),
                                          client_api=self._client_api,
                                          project=project_to_deploy)

    def delete(self, package: entities.Package = None, package_name=None, package_id=None):
        """
        Delete Package object

        :param package:
        :param package_name:
        :param package_id:
        :return: True
        """
        # get id and name
        if package_name is None or package_id is None:
            if package is None:
                package = self.get(package_id=package_id, package_name=package_name)
            package_id = package.id

        # check if project exist
        project_exists = True
        if self._project is None:
            try:
                if package is not None and package.project is not None:
                    self._project = package.project
                else:
                    self._project = repositories.Projects(client_api=self._client_api).get(
                        project_id=package.project_id)
            except exceptions.NotFound:
                project_exists = False

        if project_exists:
            # TODO can remove? in transactor?
            try:
                # create codebases repo
                codebases = repositories.Codebases(client_api=self._client_api, project=self._project)
                # get package codebases
                codebase_pages = codebases.list_versions(codebase_name=package_name)
                for codebase_page in codebase_pages:
                    for codebase in codebase_page:
                        codebase.delete()
            except exceptions.Forbidden:
                logger.debug('Failed to delete code-bases. Continue without')

        # request
        success, response = self._client_api.gen_request(
            req_type="delete",
            path="/packages/{}".format(package_id)
        )

        # exception handling
        if not success:
            raise exceptions.PlatformException(response)

        # return results
        return True

    def update(self, package: entities.Package, revision_increment: str = None) -> entities.Package:
        """
        Update Package changes to platform

        :param revision_increment: optional - str - version bumping method - major/minor/patch - default = None
        :param package:
        :return: Package entity
        """

        if revision_increment is not None and isinstance(package.version, str) and len(package.version.split('.')) == 3:
            major, minor, patch = package.version.split('.')
            if revision_increment == 'patch':
                patch = int(patch) + 1
            elif revision_increment == 'minor':
                minor = int(minor) + 1
            elif revision_increment == 'major':
                major = int(major) + 1
            package.version = '{}.{}.{}'.format(major, minor, patch)

        # payload
        payload = package.to_json()

        # request
        success, response = self._client_api.gen_request(req_type='patch',
                                                         path='/packages/{}'.format(package.id),
                                                         json_req=payload)

        # exception handling
        if not success:
            raise exceptions.PlatformException(response)

        # return entity
        return entities.Package.from_json(_json=response.json(),
                                          client_api=self._client_api,
                                          project=self._project)

    def deploy(self,
               package_id=None,
               package_name=None,
               package=None,
               service_name=None,
               project_id=None,
               revision=None,
               init_input=None,
               runtime=None,
               sdk_version=None,
               agent_versions=None,
               bot=None,
               pod_type=None,
               verify=True,
               checkout=False,
               module_name=None,
               run_execution_as_process=None,
               execution_timeout=None,
               drain_time=None,
               on_reset=None,
               max_attempts=None,
               force=False,
               **kwargs) -> entities.Service:
        """
        Deploy package

        :param max_attempts: Maximum execution retries in-case of a service reset
        :param project_id:
        :param module_name:
        :param checkout:
        :param pod_type:
        :param bot:
        :param drain_time:
        :param execution_timeout:
        :param run_execution_as_process:
        :param on_reset:
        :param init_input:
        :param force: optional - terminate old replicas immediately
        :param verify:
        :param agent_versions: - dictionary - - optional -versions of sdk, agent runner and agent proxy
        :param sdk_version:  - optional - string - sdk version
        :param runtime:
        :param revision:
        :param service_name:
        :param package:
        :param package_id:
        :param package_name:
        :return:
        """

        if package is None:
            package = self.get(package_id=package_id, package_name=package_name)

        return package.services.deploy(package=package,
                                       service_name=service_name,
                                       revision=revision,
                                       init_input=init_input,
                                       runtime=runtime,
                                       sdk_version=sdk_version,
                                       agent_versions=agent_versions,
                                       project_id=project_id,
                                       pod_type=pod_type,
                                       bot=bot,
                                       verify=verify,
                                       module_name=module_name,
                                       checkout=checkout,
                                       jwt_forward=kwargs.get('jwt_forward', None),
                                       is_global=kwargs.get('is_global', None),
                                       run_execution_as_process=run_execution_as_process,
                                       execution_timeout=execution_timeout,
                                       drain_time=drain_time,
                                       on_reset=on_reset,
                                       max_attempts=max_attempts,
                                       force=force
                                       )

    @staticmethod
    def generate(name=None, src_path=None, service_name=None, package_type=PackageCatalog.DEFAULT_PACKAGE_TYPE):
        """
        Generate new package environment

        :return:
        """
        # name
        if name is None:
            name = 'default-package'
        if service_name is None:
            service_name = 'default-service'

        # src path
        if src_path is None:
            src_path = os.getcwd()

        package_asset = Packages._package_json_generator(package_name=name, package_catalog=package_type)

        to_generate = [
            {'src': assets.paths.ASSETS_GITIGNORE_FILEPATH, 'dst': os.path.join(src_path, '.gitignore'),
             'type': 'copy'},
            {'src': package_asset,
             'dst': os.path.join(src_path, assets.paths.PACKAGE_FILENAME), 'type': 'json'},
            {'src': Packages._service_json_generator(package_catalog=package_type,
                                                     package_name=name,
                                                     service_name=service_name),
             'dst': os.path.join(src_path, assets.paths.SERVICE_FILENAME), 'type': 'json'}
        ]

        if package_type == PackageCatalog.DEFAULT_PACKAGE_TYPE:
            to_generate.append({'src': assets.paths.ASSETS_MOCK_FILEPATH,
                                'dst': os.path.join(src_path, assets.paths.MOCK_FILENAME), 'type': 'copy'})
        else:
            module = entities.PackageModule.from_json(package_asset['modules'][0])
            function_name = module.functions[0].name

            to_generate.append({'src': Packages._mock_json_generator(module=module, function_name=function_name),
                                'dst': os.path.join(src_path, assets.paths.MOCK_FILENAME), 'type': 'json'})

        main_file_paths = Packages._entry_point_generator(package_catalog=package_type)
        if len(main_file_paths) == 1:
            to_generate.append({'src': main_file_paths[0],
                                'dst': os.path.join(src_path, assets.paths.MAIN_FILENAME),
                                'type': 'copy'})
        else:
            to_generate += [{'src': main_file_paths[0],
                             'dst': os.path.join(src_path, assets.paths.MODULE_A_FILENAME),
                             'type': 'copy'},
                            {'src': main_file_paths[1],
                             'dst': os.path.join(src_path, assets.paths.MODULE_B_FILENAME),
                             'type': 'copy'}
                            ]

        for job in to_generate:
            if not os.path.isfile(job['dst']):
                if job['type'] == 'copy':
                    copyfile(job['src'], job['dst'])
                elif job['type'] == 'json':
                    with open(job['dst'], 'w') as f:
                        json.dump(job['src'], f)

        logger.info('Successfully generated package')

    @staticmethod
    def _mock_json_generator(module: entities.PackageModule, function_name):
        _json = dict(function_name=function_name, module_name=module.name)
        funcs = [func for func in module.functions if func.name == function_name]
        if len(funcs) == 1:
            func = funcs[0]
        else:
            raise exceptions.PlatformException('400', 'Other than 1 functions by the name of: {}'.format(function_name))
        _json['config'] = {inpt.name: entities.Package._mockify_input(input_type=inpt.type)
                           for inpt in module.init_inputs}
        _json['inputs'] = [{'name': inpt.name, 'value': entities.Package._mockify_input(input_type=inpt.type)}
                           for inpt in func.inputs]
        return _json

    @staticmethod
    def _package_json_generator(package_catalog, package_name):
        if package_catalog == PackageCatalog.DEFAULT_PACKAGE_TYPE:
            with open(assets.paths.ASSETS_PACKAGE_FILEPATH, 'r') as f:
                package_asset = json.load(f)
            package_asset['name'] = package_name
            return package_asset

        item_input = entities.FunctionIO(name='item', type='Item')
        annotation_input = entities.FunctionIO(name='annotation', type='Annotation')
        dataset_input = entities.FunctionIO(name='dataset', type='Dataset')
        json_input = entities.FunctionIO(name='config', type='Json')
        query_input = entities.FunctionIO(name='query', type='Json')

        func = entities.PackageFunction(name=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME)
        if package_catalog in [PackageCatalog.SINGLE_FUNCTION_ITEM, PackageCatalog.SINGLE_FUNCTION_ITEM_WITH_TRIGGER]:
            func.inputs = [item_input]
            modules = entities.PackageModule(functions=[func])
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_ANNOTATION,
                                 PackageCatalog.SINGLE_FUNCTION_ANNOTATION_WITH_TRIGGER]:
            func.inputs = [annotation_input]
            modules = entities.PackageModule(functions=[func])
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_DATASET,
                                 PackageCatalog.SINGLE_FUNCTION_DATASET_WITH_TRIGGER]:
            func.inputs = [dataset_input]
            modules = entities.PackageModule(functions=[func])
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_NO_INPUT]:
            modules = entities.PackageModule(functions=[func])
        elif package_catalog == PackageCatalog.SINGLE_FUNCTION_JSON:
            func.inputs = json_input
            modules = entities.PackageModule(functions=[func])
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_ITEM, PackageCatalog.MULTI_FUNCTION_ITEM_WITH_TRIGGERS]:
            func.inputs = [item_input]
            func.name = 'first_method'
            second_func = deepcopy(func)
            second_func.name = 'second_method'
            modules = entities.PackageModule(functions=[func, second_func])
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_ANNOTATION,
                                 PackageCatalog.MULTI_FUNCTION_ANNOTATION_WITH_TRIGGERS]:
            func.inputs = [annotation_input]
            func.name = 'first_method'
            second_func = deepcopy(func)
            second_func.name = 'second_method'
            modules = entities.PackageModule(functions=[func, second_func])
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_DATASET,
                                 PackageCatalog.MULTI_FUNCTION_DATASET_WITH_TRIGGERS]:
            func.inputs = [dataset_input]
            func.name = 'first_method'
            second_func = deepcopy(func)
            second_func.name = 'second_method'
            modules = entities.PackageModule(functions=[func, second_func])
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_JSON]:
            func.inputs = [json_input]
            func.name = 'first_method'
            second_func = deepcopy(func)
            second_func.name = 'second_method'
            modules = entities.PackageModule(functions=[func, second_func])
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_NO_INPUT]:
            func.name = 'first_method'
            second_func = deepcopy(func)
            second_func.name = 'second_method'
            modules = entities.PackageModule(functions=[func, second_func])
        elif package_catalog in [PackageCatalog.MULTI_MODULE, PackageCatalog.MULTI_MODULE_WITH_TRIGGER]:
            module_a = entities.PackageModule(functions=[func],
                                              name='first_module',
                                              entry_point='first_module_class.py')
            module_b = entities.PackageModule(functions=[func],
                                              name='second_module',
                                              entry_point='second_module_class.py')
            modules = [module_a, module_b]
        elif package_catalog == PackageCatalog.SINGLE_FUNCTION_MULTI_INPUT:
            func.inputs = [item_input, dataset_input, json_input, annotation_input]
            modules = entities.PackageModule(functions=[func])
        elif package_catalog == PackageCatalog.CONVERTER_FUNCTION:
            func.inputs = [dataset_input, query_input]
            modules = entities.PackageModule(functions=[func])
        else:
            raise exceptions.PlatformException('404', 'Unknown package catalog type: {}'.format(package_catalog))

        if not isinstance(modules, list):
            modules = [modules]

        _json = {'name': package_name,
                 'modules': [module.to_json() for module in modules]}

        return _json

    @staticmethod
    def _service_json_generator(package_catalog, package_name, service_name):
        triggers = list()
        with open(assets.paths.ASSETS_SERVICE_FILEPATH, 'r') as f:
            service_json = json.load(f)[0]
        if package_catalog == PackageCatalog.DEFAULT_PACKAGE_TYPE:
            triggers = service_json['triggers']
        elif 'triggers' in package_catalog:
            trigger_a = dict(name='first_trigger', filter=dict(), actions=['Created'], function='first_method',
                             executionMode='Once')
            trigger_b = dict(name='second_trigger', filter=dict(), actions=['Created'], function='second_method',
                             executionMode='Once')
            if 'item' in package_catalog:
                trigger_a['resource'] = trigger_b['resource'] = 'Item'
            if 'dataset' in package_catalog:
                trigger_a['resource'] = trigger_b['resource'] = 'Dataset'
            if 'annotation' in package_catalog:
                trigger_a['resource'] = trigger_b['resource'] = 'Annotation'
            triggers += [trigger_a, trigger_b]
        elif 'trigger' in package_catalog:
            trigger = dict(name='trigger_name',
                           filter=dict(),
                           actions=[],
                           function=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME,
                           executionMode='Once')
            if 'item' in package_catalog:
                trigger['resource'] = 'Item'
            if 'dataset' in package_catalog:
                trigger['resource'] = 'Dataset'
            if 'annotation' in package_catalog:
                trigger['resource'] = 'Annotation'
            triggers += [trigger]

        if service_name is not None:
            service_json['name'] = service_name
        if package_name is not None:
            service_json['packageName'] = package_name
        if 'multi_module' in package_catalog:
            service_json['moduleName'] = 'first_module'

        service_json['triggers'] = triggers

        return service_json

    @staticmethod
    def _entry_point_generator(package_catalog):
        if package_catalog == PackageCatalog.DEFAULT_PACKAGE_TYPE:
            paths_to_service_runner = assets.paths.ASSETS_MAIN_FILEPATH
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_ITEM, PackageCatalog.SINGLE_FUNCTION_ITEM_WITH_TRIGGER]:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_ITEM_SR_PATH
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_ANNOTATION,
                                 PackageCatalog.SINGLE_FUNCTION_ANNOTATION_WITH_TRIGGER]:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_ANNOTATION_SR_PATH
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_DATASET,
                                 PackageCatalog.SINGLE_FUNCTION_DATASET_WITH_TRIGGER]:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_DATASET_SR_PATH
        elif package_catalog in [PackageCatalog.SINGLE_FUNCTION_NO_INPUT]:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_SR_PATH
        elif package_catalog == PackageCatalog.SINGLE_FUNCTION_JSON:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_JSON_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_ITEM, PackageCatalog.MULTI_FUNCTION_ITEM_WITH_TRIGGERS]:
            paths_to_service_runner = assets.service_runner_paths.MULTI_METHOD_ITEM_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_ANNOTATION,
                                 PackageCatalog.MULTI_FUNCTION_ANNOTATION_WITH_TRIGGERS]:
            paths_to_service_runner = assets.service_runner_paths.MULTI_METHOD_ANNOTATION_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_DATASET,
                                 PackageCatalog.MULTI_FUNCTION_DATASET_WITH_TRIGGERS]:
            paths_to_service_runner = assets.service_runner_paths.MULTI_METHOD_DATASET_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_JSON]:
            paths_to_service_runner = assets.service_runner_paths.MULTI_METHOD_JSON_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_FUNCTION_NO_INPUT]:
            paths_to_service_runner = assets.service_runner_paths.MULTI_METHOD_SR_PATH
        elif package_catalog in [PackageCatalog.MULTI_MODULE, PackageCatalog.MULTI_MODULE_WITH_TRIGGER]:
            paths_to_service_runner = [assets.service_runner_paths.SINGLE_METHOD_ITEM_SR_PATH,
                                       assets.service_runner_paths.SINGLE_METHOD_ITEM_SR_PATH]
        elif package_catalog == PackageCatalog.SINGLE_FUNCTION_MULTI_INPUT:
            paths_to_service_runner = assets.service_runner_paths.SINGLE_METHOD_MULTI_INPUT_SR_PATH
        elif package_catalog == PackageCatalog.CONVERTER_FUNCTION:
            paths_to_service_runner = assets.service_runner_paths.CONVERTER_SR_PATH
        else:
            raise exceptions.PlatformException('404', 'Unknown package catalog type: {}'.format(package_catalog))

        if not isinstance(paths_to_service_runner, list):
            paths_to_service_runner = [paths_to_service_runner]

        return paths_to_service_runner

    @staticmethod
    def is_multithread(inputs):
        is_multi = False
        if len(inputs) > 0 and isinstance(inputs[0], list):
            is_multi = True

        if is_multi:
            for single_input in inputs:
                if not isinstance(single_input, list):
                    raise exceptions.PlatformException('400', 'mock.json inputs can be either list of dictionaries '
                                                              'or list of lists')

        return is_multi

    def test_local_package(self,
                           cwd=None,
                           concurrency=None,
                           package: entities.Package = None,
                           module_name=entities.package_defaults.DEFAULT_PACKAGE_MODULE_NAME,
                           function_name=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME,
                           class_name=entities.package_defaults.DEFAULT_PACKAGE_CLASS_NAME,
                           entry_point=entities.package_defaults.DEFAULT_PACKAGE_ENTRY_POINT):
        """
        Test local package
        :return:
        """
        if cwd is None:
            cwd = os.getcwd()

        with open(os.path.join(cwd, assets.paths.MOCK_FILENAME), 'r') as f:
            mock_json = json.load(f)
        is_multithread = self.is_multithread(inputs=mock_json['inputs'])

        local_runner = LocalServiceRunner(self._client_api,
                                          packages=self,
                                          cwd=cwd,
                                          package=package,
                                          multithreading=is_multithread,
                                          concurrency=concurrency,
                                          module_name=module_name,
                                          function_name=function_name,
                                          class_name=class_name,
                                          entry_point=entry_point)

        if self._project is None:
            try:
                project = repositories.Projects(client_api=self._client_api).get()
            except Exception:
                project = None
        else:
            project = self.project

        return local_runner.run_local_project(project=project)

    def __get_from_cache(self) -> entities.Package:
        package = self._client_api.state_io.get('package')
        if package is not None:
            package = entities.Package.from_json(_json=package, client_api=self._client_api, project=self._project)
        return package

    def checkout(self, package=None, package_id=None, package_name=None):
        """
        Checkout as package

        :param package_id:
        :param package:
        :param package_name:
        :return:
        """
        if package is None:
            package = self.get(package_id=package_id, package_name=package_name)
        self._client_api.state_io.put('package', package.to_json())
        logger.info("Checked out to package {}".format(package.name))

    @staticmethod
    def _sanity_before_push(src_path, modules):
        if modules is None:
            modules = [DEFAULT_PACKAGE_MODULE]

        if not isinstance(modules, list):
            modules = [modules]

        if not isinstance(modules[0], entities.PackageModule):
            modules = [entities.PackageModule.from_json(_json=module) for module in modules]

        missing = list()
        for module in modules:
            entry_point = module.entry_point
            class_name = module.class_name

            check_init = True
            functions = module.functions
            # check in inputs is a list
            if not isinstance(functions, list):
                functions = [functions]

            for function in functions:
                # entry point exists
                entry_point_filepath = os.path.join(src_path, entry_point)
                if not os.path.isfile(entry_point_filepath):
                    missing.append('missing entry point file: {}'.format(entry_point_filepath))
                    continue

                # class name in entry point
                try:
                    spec = importlib.util.spec_from_file_location(class_name, entry_point_filepath)
                    foo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(foo)
                except ImportError as e:
                    logger.warning(
                        'Cannot run sanity check to find conflicts between package module and source code'
                        'because some packages in your source code are not installed in your local environment'.format(
                            e.__str__())
                    )
                    return modules

                if not hasattr(foo, class_name):
                    missing.append('missing class: "{}" from file: "{}"'.format(class_name, entry_point_filepath))
                    continue

                # function in class
                cls = getattr(foo, class_name)
                if not hasattr(cls, function.name):
                    missing.append(
                        'missing function: "{}" from class: "{}"'.format(function.name, entry_point_filepath))
                    continue

                if check_init:
                    check_init = False
                    # input to __init__ and inputs definitions match
                    func = getattr(cls, "__init__")
                    func_inspect = inspect.getfullargspec(func)
                    defined_input_names = [inp.name for inp in module.init_inputs]
                    for input_name in func_inspect.args:
                        if input_name in ['self', 'progress']:
                            continue
                        if input_name not in defined_input_names:
                            missing.append('missing input name: "{}" in function definition: "{}"'.format(input_name,
                                                                                                          "__init__"))

                # input to function and inputs definitions match
                func = getattr(cls, function.name)
                func_inspect = inspect.getfullargspec(func)
                inputs = function.inputs
                if not isinstance(inputs, list):
                    inputs = [inputs]
                defined_input_names = [inp.name for inp in inputs]
                for input_name in func_inspect.args:
                    if input_name in ['self', 'progress']:
                        continue
                    if input_name not in defined_input_names:
                        missing.append(
                            'missing input name: "{}" in function definition: "{}"'.format(input_name, function.name))

        if len(missing) != 0:
            raise ValueError('There are conflicts between modules and source code:'
                             '\n{}\n{}'.format(missing,
                                               'Please fix conflicts or use flag ignore_sanity_check'))
        return modules


class LocalServiceRunner:
    """
    Service Runner Class
    """

    def __init__(self,
                 client_api: services.ApiClient,
                 packages,
                 cwd=None,
                 multithreading=False,
                 concurrency=10,
                 package: entities.Package = None,
                 module_name=entities.package_defaults.DEFAULT_PACKAGE_MODULE_NAME,
                 function_name=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME,
                 class_name=entities.package_defaults.DEFAULT_PACKAGE_CLASS_NAME,
                 entry_point=entities.package_defaults.DEFAULT_PACKAGE_ENTRY_POINT):
        if cwd is None:
            self.cwd = os.getcwd()
        else:
            self.cwd = cwd

        self._client_api = client_api
        self._packages = packages
        self.package_io = PackageIO(cwd=self.cwd)
        self.multithreading = multithreading
        self.concurrency = concurrency
        self._module_name = module_name
        self._function_name = function_name
        self._entry_point = entry_point
        self._class_name = class_name
        self.package = package

        with open(os.path.join(self.cwd, 'mock.json'), 'r') as f:
            self.mock_json = json.load(f)

    @property
    def function_name(self):
        return self.mock_json.get('function_name', self._function_name)

    @property
    def module_name(self):
        return self.mock_json.get('module_name', self._module_name)

    @property
    def class_name(self):
        return self.mock_json.get('class_name', self._class_name)

    @property
    def entry_point(self):
        return self.mock_json.get('entry_point', self._entry_point)

    def get_mainpy_run_service(self):
        """
        Get mainpy run service
        :return:
        """
        entry_point = os.path.join(self.cwd, self.entry_point)
        spec = importlib.util.spec_from_file_location(self.class_name, entry_point)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        service_runner = getattr(foo, self.class_name)

        if 'init_params' in self.mock_json:
            kwargs = self.mock_json.get('init_params')
        elif 'config' in self.mock_json:
            kwargs = self.mock_json.get('config')
        else:
            kwargs = dict()

        return service_runner(**kwargs)

    def run_local_project(self, project=None):
        package_runner = self.get_mainpy_run_service()

        modules = self.package_io.get('modules') if self.package is None else [
            m.to_json() for m in self.package.modules
        ]

        if isinstance(modules, list) and len(modules) > 0:
            try:
                module = [module for module in modules if module['name'] == self.module_name][0]
            except Exception:
                raise exceptions.PlatformException(
                    '400', 'Module {} does not exist in package modules'.format(self.module_name)
                )
        else:
            module = DEFAULT_PACKAGE_MODULE.to_json()

        if isinstance(module['functions'], list) and len(module['functions']) > 0:
            try:
                func = [func for func in module['functions'] if func['name'] == self.function_name][0]
            except Exception:
                raise exceptions.PlatformException(
                    '400', 'function {} does not exist in package module'.format(self.function_name)
                )
        else:
            func = entities.PackageFunction(None, list(), list(), None).to_json()
        package_inputs = func['input']
        current_level = logging.root.level
        logging.root.setLevel('INFO')
        if not self.multithreading:
            kwargs = dict()
            progress = utilities.Progress()

            func = getattr(package_runner, self.function_name)
            params = list(inspect.signature(func).parameters)
            if "progress" in params:
                kwargs['progress'] = progress

            for package_input in package_inputs:
                kwargs[package_input['name']] = self.get_field(field_name=package_input['name'],
                                                               field_type=package_input['type'],
                                                               project=project, mock_json=self.mock_json)

            results = getattr(package_runner, self.function_name)(**kwargs)
        else:
            pool = ThreadPool(processes=self.concurrency)
            inputs = self.mock_json['inputs']
            results = list()
            jobs = list()
            for single_input in inputs:
                kwargs = dict()
                progress = utilities.Progress()
                kwargs['progress'] = progress
                for package_input in package_inputs:
                    kwargs[package_input['name']] = self.get_field(field_name=package_input['name'],
                                                                   field_type=package_input['type'],
                                                                   project=project,
                                                                   mock_json=self.mock_json,
                                                                   mock_inputs=single_input)
                jobs.append(
                    pool.apply_async(
                        func=getattr(package_runner, self.function_name),
                        kwds=kwargs
                    )
                )
            for job in jobs:
                job.wait()
                results.append(job.get())

        logging.root.level = current_level
        return results

    def get_dataset(self, resource_id, project=None) -> entities.Dataset:
        """
        Get dataset
        :param project:
        :param resource_id:
        :return: Dataset entity
        """
        dataset_id = resource_id.get('dataset_id', None) if isinstance(resource_id, dict) else resource_id

        if not isinstance(dataset_id, str):
            dataset_id = self._client_api.state_io.get('dataset')

        if project is not None:
            datasets = project.datasets
        else:
            datasets = repositories.Datasets(client_api=self._client_api)

        return datasets.get(dataset_id=dataset_id)

    def get_item(self, resource_id, project=None) -> entities.Item:
        """
        Get item
        :param project:
        :param resource_id:
        :return: Item entity
        """
        if project is not None:
            items = project.items
        else:
            items = repositories.Items(client_api=self._client_api)

        return items.get(item_id=resource_id['item_id'] if isinstance(resource_id, dict) else resource_id)

    def get_annotation(self, resource_id, project=None) -> entities.Annotation:
        """
        Get annotation
        :param project:
        :param resource_id:
        :return: Annotation entity
        """
        item = self.get_item(project=project, resource_id=resource_id)
        return item.annotations.get(
            annotation_id=resource_id['annotation_id'] if isinstance(resource_id, dict) else resource_id)

    def get_field(self, field_name, field_type, mock_json, project=None, mock_inputs=None):
        """
        Get field in mock json
        :param field_name:
        :param field_type:
        :param project:
        :param mock_json:
        :param mock_inputs:
        :return:
        """
        if mock_inputs is None:
            mock_inputs = mock_json['inputs']
        filtered_mock_inputs = list(filter(lambda input_field: input_field['name'] == field_name, mock_inputs))

        if len(filtered_mock_inputs) == 0:
            raise Exception('No entry for field {} found in mock'.format(field_name))
        if len(filtered_mock_inputs) > 1:
            raise Exception('Duplicate entries for field {} found in mock'.format(field_name))

        mock_input = filtered_mock_inputs[0]
        resource_id = mock_input['value']

        if field_type == 'Dataset':
            return self.get_dataset(project=project, resource_id=resource_id)

        elif field_type == 'Item':
            return self.get_item(project=project, resource_id=resource_id)

        elif field_type == 'Annotation':
            return self.get_annotation(project=project, resource_id=resource_id)

        elif field_type == 'Json':
            return mock_input['value']

        else:
            raise exceptions.PlatformException('400', 'Unknown resource type for field {}'.format(field_name))


class PackageIO:

    def __init__(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()

        self.package_file_path = os.path.join(cwd, assets.paths.PACKAGE_FILENAME)
        self.service_file_path = os.path.join(cwd, assets.paths.SERVICE_FILENAME)

    def read_json(self, resource='package'):
        if resource == 'package':
            file_path = self.package_file_path
        else:
            file_path = self.service_file_path

        with open(file_path, 'r') as fp:
            cfg = json.load(fp)
        return cfg

    def get(self, key, resource='package'):
        cfg = self.read_json(resource=resource)
        return cfg[key]

    def put(self, key, value, resource='package'):
        try:
            cfg = self.read_json(resource=resource)
            cfg[key] = value

            if resource == 'package':
                file_path = self.package_file_path
            else:
                file_path = self.service_file_path

            with open(file_path, 'w') as fp:
                json.dump(cfg, fp, indent=2)
        except Exception:
            pass
