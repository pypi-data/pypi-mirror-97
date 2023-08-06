from typing import Dict, Any, Optional, List, FrozenSet, Callable

from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.services import AuthorizationService, RestService, AuthorizationHttpService, HttpService

from vtb_authorizer_utils.converters import convert_user, convert_organization, convert_project, \
    convert_folder, convert_children
from vtb_authorizer_utils.data_objects import User, Organization, Project, Folder, Children
from vtb_authorizer_utils.errors import NotAllowedParameterError


class AuthorizerGateway:
    def __init__(self, base_url: str,
                 keycloak_config: Optional[KeycloakConfig] = None,
                 redis_connection_string: Optional[str] = None,
                 access_token: Optional[str] = None):
        if keycloak_config is None and access_token is None:
            raise ValueError("keycloak_config is none and access_token is none. You must specify something.")

        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}

        self.service = HttpService() if access_token else AuthorizationHttpService(keycloak_config,
                                                                                   redis_connection_string)

    """"""""" Пользователи """""""""

    async def get_user(self, keycloak_id: str) -> Optional[User]:
        """ Получение пользователя по keycloak_id (Keycloak ID) """
        return await self._get_item([_users_url], keycloak_id, convert_user)

    async def get_users(self, **query_params) -> Optional[List[User]]:
        """ Получение списка пользователей """
        _check_request(query_params, _users_allowed_parameters)

        return await self._get_list([_users_url], convert_user, **query_params)

    """"""""" Организации """""""""

    async def get_organization(self, name: str) -> Optional[Organization]:
        """ Получение организации по name (кодовое название) """
        return await self._get_item([_organizations_url], name, convert_organization)

    async def get_organizations(self, **query_params) -> Optional[List[Organization]]:
        """ Получение списка организаций """
        _check_request(query_params, _organizations_allowed_parameters)

        return await self._get_list([_organizations_url], convert_organization, **query_params)

    async def get_organization_projects(self, name: str, **query_params) -> Optional[List[Project]]:
        """ Получение проектов организации """
        _check_request(query_params, _organization_projects_allowed_parameters)

        return await self._get_list([_organizations_url, name, _projects_url], convert_project,
                                    **query_params)

    async def get_organization_children(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение потомков организации """

        return await self._get_list([_organizations_url, name, 'children'], convert_children,
                                    **query_params)

    """"""""" Folders """""""""

    async def get_folder(self, name: str) -> Optional[Folder]:
        """ Получение папки по name """
        return await self._get_item([_folders_url], name, convert_folder)

    """"""""" Projects """""""""

    async def get_project(self, name: str) -> Optional[Project]:
        """ Получение проекта по name """
        return await self._get_item([_projects_url], name, convert_project)

    """"""""" private """""""""

    async def _get_item(self, url_path: List[str], item_id: Any, converter: Callable[[Dict[str, Any]], Any]) -> \
            Optional[Any]:
        """ Получение объекта """
        request = {
            'method': "GET",
            'url': _join_str(self.base_url, *url_path, str(item_id)),
            'cfg': {'headers': self.headers}
        }
        status, response = await self.service.send_request(**request)

        return converter(response['data']) if status == 200 else None

    async def _get_list(self, url_path: List[str], converter: Callable[[Dict[str, Any]], Any],
                        **query_params) -> Optional[List]:
        """ Получение списка объектов """
        request = {
            'method': "GET",
            'url': _join_str(self.base_url, *url_path),
            'cfg': {'params': query_params, 'headers': self.headers}
        }
        status, response = await self.service.send_request(**request)

        return list(map(converter, response['data'])) if status == 200 else None


_users_allowed_parameters = frozenset({"page", "per_page", "q", "username", "firstname", "lastname", "email"})
_users_url = 'users'

_organizations_allowed_parameters = frozenset({"page", "per_page", "include"})
_organization_projects_allowed_parameters = frozenset({"page", "per_page", "include"})
_organizations_url = 'organizations'

_folders_url = 'folders'
_projects_url = 'projects'


def _check_request(query_params: Dict[str, Any], allowed_parameters: FrozenSet[str]):
    """ Проверка параметров запроса """
    keys = frozenset(query_params.keys())
    not_allowed_parameters = keys - allowed_parameters
    if len(not_allowed_parameters) > 0:
        raise NotAllowedParameterError(not_allowed_parameters, allowed_parameters)


def _join_str(*args, sep: Optional[str] = '/') -> str:
    return sep.join(arg.strip(sep) for arg in args)
