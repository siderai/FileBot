from typing import ClassVar, Type, List, Any
from dataclasses import field
from json import JSONDecodeError

import aiohttp
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE, ValidationError

from clients.tg.api import TgClient, TgClientError
from clients.tg.dcs import File, Message, GetFileResponse, SendMessageResponse


class TgClientWithFile(TgClient):
    BASE_FILE_PATH = "https://api.telegram.org/file/bot"

    def __init__(self, token):
        super().__init__(self)
        self.token = token

    def get_path(self, url: str, is_file: bool = True) -> str:
        base_path = (
            self.BASE_FILE_PATH.strip("/")
            if is_file
            else self.get_base_path().strip("/")
        )
        url = url.lstrip("/")
        return f"{base_path}{self.token}/{url}"

    async def _handle_response(self, resp: aiohttp.ClientResponse) -> Any:
        if resp.status != 200:
            raise TgClientError(resp, await resp.text())
        try:
            return await resp.json()
        except aiohttp.client_exceptions.ContentTypeError:
            return await resp.read()
        except JSONDecodeError:
            raise TgClientError(resp, await resp.text())

    async def get_file(self, file_id: str) -> File:
        data = await self._perform_request(
            "get", self.get_path("getFile", is_file=False), params={"file_id": file_id}
        )
        try:
            resp = GetFileResponse.Schema().load(data)
        except ValidationError:
            raise TgClientError(None, None)
        file_: File = resp.result
        return file_

    async def download_file(self, file_path: str, destination_path: str):
        resp: aiohttp.ClientResponse = await self._perform_request(
            "get", self.get_path(file_path)
        )
        with open(destination_path, "wb") as fd:
            fd.write(resp)

    async def send_document(self, chat_id: int, document_path) -> Message:
        with open(document_path, "rb") as document:
            data = aiohttp.FormData()
            data.add_field("document", document, content_type="text/plain")

        params = {"chat_id": chat_id}
        resp: Message = await self._perform_request(
            "post", self.get_path("sendDocument", is_file=False), json=params, data=data
        )
        try:
            sm_response: SendMessageResponse = SendMessageResponse.Schema().load(resp)
        except ValidationError:
            raise TgClientError(None, None)
        return sm_response.result
