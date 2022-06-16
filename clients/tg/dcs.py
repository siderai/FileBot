rom typing import ClassVar, Type, List, Any, Optional
from dataclasses import field

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE



@dataclass
class Chat:
    id: int = field(metadata={'data_key': 'id'})
    type: str = field(metadata={'data_key': 'type'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class User:
    id: int = field(metadata={'data_key': 'id'})
    username: str = field(metadata={'data_key': 'username'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class Document:
    file_name: str = field(metadata={'data_key': 'file_name'})
    file_id: str = field(metadata={'data_key': 'file_id'})
    file_size: int = field(metadata={'data_key': 'file_size'})
    file_unique_id: str = field(metadata={'data_key': 'file_unique_id'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class File:
    file_id: str = field(metadata={'data_key': 'file_id'})
    file_size: int = field(metadata={'data_key': 'file_size'})
    file_path: str = field(metadata={'data_key': 'file_path'})
    file_unique_id: str = field(metadata={'data_key': 'file_unique_id'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class GetFileResponse:
    ok: bool = field(metadata={'data_key': 'ok'})
    result: File = field(metadata={'data_key': 'result'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class Message:
    message_id: int = field(metadata={'data_key': 'message_id'})
    date: int = field(metadata={'data_key': 'date'})
    chat: Chat = field(metadata={'data_key': 'chat'})
    from_: Optional[User] = field(metadata={'data_key': 'from'})
    text: Optional[str] = field(metadata={'data_key': 'text'})
    document: Optional[Document] = field(metadata={'data_key': 'document'})
    file: Optional[File] = field(metadata={'data_key': 'file'})
    
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

@dataclass
class UpdateObj:
    update_id: int = field(metadata={'data_key': 'update_id'})
    message: Message = field(metadata={'data_key': 'message'})

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

