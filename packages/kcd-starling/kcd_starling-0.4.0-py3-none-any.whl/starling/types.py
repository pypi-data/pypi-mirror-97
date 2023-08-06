import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Union, List, Dict, Text, Any

if TYPE_CHECKING:
    pass


@dataclass
class ScrapperData:
    id: str
    topic: str
    candidate: Any
    message: 'MessageData'
    source: str = None
    actions: Dict[str, List['TaskData']] = field(default_factory=dict)
    auth_session: Any = None
    error_message: str = None
    error_extra: dict = None
    is_valid: bool = True
    extra_config: dict = field(default_factory=dict)
    broadcast_variables: dict = field(default_factory=dict)
    durations: dict = field(default_factory=dict)


@dataclass
class TaskData:
    action: str
    fetched_data: 'FetchedData' = None
    is_done: bool = False
    criteria: Dict = field(default_factory=dict)
    error: dict = field(default_factory=dict)


@dataclass()
class MessageData:
    message: dict
    created_at: str = None
    consumed_at: str = None
    scrap_started_at: str = None
    scrap_finished_at: str = None
    visibility_timeout_at: str = None


class PloverDataType(enum.Enum):
    LIST = enum.auto()
    DICT = enum.auto()
    COMBINED = enum.auto()


@dataclass()
class FetchedData:
    data: Any
    plover_data: Union[
        Dict[Text, Any], List[Dict[Text, Any]], Dict[Text, Union[Dict[Text, Any], List[Dict[Text, Any]]]]] = None
    plover_data_type: PloverDataType = PloverDataType.LIST
