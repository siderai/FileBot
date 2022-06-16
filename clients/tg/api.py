from typing import Optional, List, Any
import os
import json

from aiohttp import ClientResponse
from marshmallow import ValidationError

from clients.base import ClientError, Client
from clients.tg.dcs import UpdateObj, Message, GetUpdatesResponse, SendMessageResponse


class TgClientError(ClientError):
    def __init__(self, response: ClientResponse, content: Any = None):
        super().__init__(self)


class TgClient(Client):
    BASE_PATH = "https://api.telegram.org/bot"

    def __init__(self, token: str = ""):
        super().__init__()
        self.token = token

    def get_path(self, url: str) -> str:
        base_path = self.get_base_path().strip("/")
        url = url.lstrip("/")
        return f"{base_path}{self.token}/{url}"

    async def _handle_response(self, resp: ClientResponse) -> Any:
        if resp.status != 200:
            raise TgClientError(resp, await resp.text())
        try:
            return await resp.json()
        except Exception:
            raise TgClientError(resp, await resp.text())

    async def get_me(self) -> dict:
        return await self._perform_request("get", self.get_path("getMe"))

    async def get_updates(
        self, offset: Optional[int] = None, timeout: Optional[int] = 0
    ) -> dict:
        params = {"offset": offset, "timeout": timeout}
        non_empty_params = {k: v for k, v in params.items() if v}
        return await self._perform_request(
            "get", self.get_path("getUpdates"), params=non_empty_params
        )

    async def get_updates_in_objects(self, *args, **kwargs) -> List[UpdateObj]:
        data: List[UpdateObj] = await self._perform_request(
            "get", self.get_path("getUpdates"), params=kwargs
        )
        try:
            updates_response: GetUpdatesResponse = GetUpdatesResponse.Schema().load(
                data
            )
        except ValidationError:
            raise TgClientError(None, None)
        return updates_response.result

    async def send_message(self, chat_id: int, text: str) -> Message:
        json = {"chat_id": chat_id, "text": text}
        data = await self._perform_request(
            "post", self.get_path("sendMessage"), json=json
        )
        try:
            sm_response: SendMessageResponse = SendMessageResponse.Schema().load(data)
        except ValidationError:
            raise TgClientError(None, None)
        return sm_response.result
