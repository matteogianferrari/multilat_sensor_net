from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PS_UNKNOWN: _ClassVar[PositionStatus]
    PS_OK: _ClassVar[PositionStatus]
    PS_ERROR: _ClassVar[PositionStatus]
PS_UNKNOWN: PositionStatus
PS_OK: PositionStatus
PS_ERROR: PositionStatus

class GetPositionRequest(_message.Message):
    __slots__ = ("node_id",)
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    def __init__(self, node_id: _Optional[int] = ...) -> None: ...

class GetPositionResponse(_message.Message):
    __slots__ = ("status", "x", "y", "z")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    status: PositionStatus
    x: float
    y: float
    z: float
    def __init__(self, status: _Optional[_Union[PositionStatus, str]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...
