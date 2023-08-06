#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
from enum import Enum


class DataLayoutType(Enum):
    DATA_TEMPLATE = "template"
    DATA_CONTAINER = "container"


class EnvironmentTypes(Enum):
    UNIX = "unix"
    WIN = "windows"
    LINUX = "linux"


class EnvironmentHostTypes(Enum):
    WIN = "WindowsHostEnvironment"
    WINCLUSTER = "WindowsCluster"


class HostTypes(Enum):
    WIN = "WindowsHost"
    UNIX = "UnixHost"


class EnvironmentOps(Enum):
    ADD = "add"
    UPDATEHOST = "updatehost"
    DELETE = "delete"
    REFRESH = "refresh"
    ENABLE = "enable"
    DISABLE = "disable"
    LIST = "list"


class BranchOps(Enum):
    CREATE = "create"
    DELETE = "delete"
    ACTIVATE = "activate"
    LIST = "list"


class BookmarkOps(Enum):
    CREATE = "create"
    DELETE = "delete"
    UPDATE = "update"
    SHARE = "share"
    UNSHARE = "unshare"
    LIST = "list"


class VirtualOps(Enum):
    PROVISION = "create"
    REFRESH = "refresh"
    REWIND = "rewind"
    SNAPSHOT = "snapshot"
    START = "start"
    STOP = "stop"
    ENABLE = "enable"
    DISABLE = "disable"
    DELETE = "delete"
    LIST = "list"


class SourceOps(Enum):
    CREATE = "create"
    DELETE = "delete"
    LINK = "link"
    UNLIK = "unlink"


class TemplateOps(Enum):
    CREATE = "create"
    DELETE = "delete"
    LIST = "list"
