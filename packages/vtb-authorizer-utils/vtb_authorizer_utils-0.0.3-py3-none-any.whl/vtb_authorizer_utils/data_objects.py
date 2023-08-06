from typing import NamedTuple, Optional


class Children(NamedTuple):
    """ Потомок организации """
    name: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[str] = None
    kind: Optional[str] = None
    children_count: Optional[int] = None


class Folder(NamedTuple):
    """ Организация """
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    kind: Optional[str] = None
    organization: Optional[str] = None
    parent: Optional[str] = None
    children_count: Optional[int] = None


class Project(NamedTuple):
    """ Проект организации """
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    organization: Optional[str] = None
    folder: Optional[str] = None
    information_system_id: Optional[str] = None
    project_environment_id: Optional[str] = None
    environment_prefix_id: Optional[str] = None


class Organization(NamedTuple):
    """ Организация """
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class User(NamedTuple):
    """ Пользователь """
    # Внешний идентификатор пользователя
    remote_id: Optional[str] = None
    # Email
    email: Optional[str] = None
    # Login
    user_name: Optional[str] = None
    # Имя
    first_name: Optional[str] = None
    # Фамилия
    last_name: Optional[str] = None
