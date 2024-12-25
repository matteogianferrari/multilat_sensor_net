from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TargetStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TS_UNKNOWN: _ClassVar[TargetStatus]
    TS_OK: _ClassVar[TargetStatus]
    TS_ERROR: _ClassVar[TargetStatus]

class NodeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NS_UNKNOWN: _ClassVar[NodeStatus]
    NS_OK: _ClassVar[NodeStatus]
    NS_ERROR: _ClassVar[NodeStatus]

class SNStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SS_UNKNOWN: _ClassVar[SNStatus]
    SS_OK: _ClassVar[SNStatus]
    SS_ERROR: _ClassVar[SNStatus]
TS_UNKNOWN: TargetStatus
TS_OK: TargetStatus
TS_ERROR: TargetStatus
NS_UNKNOWN: NodeStatus
NS_OK: NodeStatus
NS_ERROR: NodeStatus
SS_UNKNOWN: SNStatus
SS_OK: SNStatus
SS_ERROR: SNStatus

class TargetRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    def __init__(self, client_id: _Optional[int] = ...) -> None: ...

class TargetResponse(_message.Message):
    __slots__ = ("status", "x", "y", "z")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    status: TargetStatus
    x: float
    y: float
    z: float
    def __init__(self, status: _Optional[_Union[TargetStatus, str]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class NodeRequest(_message.Message):
    __slots__ = ("node_id", "x", "y", "z", "bind_address")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    BIND_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    x: float
    y: float
    z: float
    bind_address: str
    def __init__(self, node_id: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., bind_address: _Optional[str] = ...) -> None: ...

class NodeResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: NodeStatus
    def __init__(self, status: _Optional[_Union[NodeStatus, str]] = ...) -> None: ...

class StartRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    def __init__(self, client_id: _Optional[int] = ...) -> None: ...

class StartResponse(_message.Message):
    __slots__ = ("status", "n_nodes")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    N_NODES_FIELD_NUMBER: _ClassVar[int]
    status: SNStatus
    n_nodes: int
    def __init__(self, status: _Optional[_Union[SNStatus, str]] = ..., n_nodes: _Optional[int] = ...) -> None: ...
