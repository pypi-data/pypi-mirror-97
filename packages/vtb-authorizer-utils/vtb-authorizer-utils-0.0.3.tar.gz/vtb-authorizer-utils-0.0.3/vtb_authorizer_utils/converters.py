from typing import Dict, Any

from vtb_authorizer_utils.data_objects import User, Organization, Project, Folder, Children


def convert_user(data: Dict[str, Any]) -> User:
    """ Конвертация ответа в data класс RemoteUser """
    return User(
        remote_id=data.get('id', None),
        email=data.get('email', None),
        user_name=data.get('username', None),
        first_name=data.get('firstname', None),
        last_name=data.get('lastname', None)
    )


def convert_organization(data: Dict[str, Any]) -> Organization:
    """ Конвертация ответа в data класс RemoteOrganization """
    return Organization(
        name=data.get('name', None),
        title=data.get('title', None),
        description=data.get('description', None)
    )


def convert_project(data: Dict[str, Any]) -> Project:
    """ Конвертация ответа в data класс Project """
    return Project(
        name=data.get('name', None),
        title=data.get('title', None),
        description=data.get('description', None),
        organization=data.get('organization', None),
        folder=data.get('folder', None),
        information_system_id=data.get('information_system_id', None),
        project_environment_id=data.get('project_environment_id', None),
        environment_prefix_id=data.get('environment_prefix_id', None)
    )


def convert_children(data: Dict[str, Any]) -> Children:
    """ Конвертация ответа в data класс Children """
    return Children(
        name=data.get('name', None),
        title=data.get('title', None),
        type=data.get('type', None),
        parent=data.get('parent', None),
        kind=data.get('kind', None),
        children_count=data.get('children_count', None)
    )


def convert_folder(data: Dict[str, Any]) -> Folder:
    """ Конвертация ответа в data класс Folder """
    return Folder(
        name=data.get('name', None),
        title=data.get('title', None),
        description=data.get('description', None),
        kind=data.get('kind', None),
        organization=data.get('organization', None),
        parent=data.get('parent', None),
        children_count=data.get('children_count', None)
    )
