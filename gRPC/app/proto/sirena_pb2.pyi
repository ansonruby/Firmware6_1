from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("priority",)
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    priority: int
    def __init__(self, priority: _Optional[int] = ...) -> None: ...
