import asyncio
from typing import Optional, List

from clients.tg.api import TgClient
from bot.utils import log_exceptions


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    # @log_exceptions
    async def _worker(self):
        """
        нужно получать данные из tg, стоит использовать метод get_updates_in_objects
        полученные сообщения нужно положить в очередь queue
        в очередь queue нужно класть UpdateObj
        """
        offset = 0
        while self.is_running:
            res: List[UpdateObj] = await self.tg_client.get_updates_in_objects(
                offset=offset, timeout=60
            )
            for update in res:
                offset = update.update_id + 1
                print(update)
                self.queue.put_nowait(update)

    def start(self):
        self.is_running = True
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        try:
            self._task.cancel()
            self.is_running = False
            await self._task
        except asyncio.exceptions.CancelledError:
            pass
