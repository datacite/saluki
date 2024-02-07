from enum import Enum, IntEnum


class DataFileType(Enum):
    """The type of data file."""

    yearly = "Yearly"
    monthly = "Monthly"
    corpus = "Corpus"
    other = "Other"


class UserLevel(IntEnum):
    """The user level."""

    anonymous = 0
    user = 1  # Can read data files as defined by permissions
    editor = 2  # Can create and edit data files
    staff = 3  # Can edit users and permissions
    admin = 4  # Can do everything


class DataFileStatus(Enum):
    """The status of a data file."""

    active = "Available"
    generating = "Generating"
    hidden = "Hidden"
    deleted = "Deleted"


class PermissionType(Enum):
    """The type of permission."""

    filetype = "filetype"
    datafile = "datafile"
