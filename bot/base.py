import asyncio
from dataclasses import dataclass

from bot.poller import Poller
from bot.worker import Worker, WorkerConfig


@dataclass
class BotConfig:
    token: str
    worker: WorkerConfig


class Bot:
    def __init__(self, config: BotConfig):
        queue = asyncio.Queue()
        self.poller = Poller(config.token, queue)
        self.worker = Worker(config.token, queue, config.worker)

    async def start(self):
        self.poller.start()
        self.worker.start()

    async def stop(self):
        await self.poller.stop()
        await self.worker.stop()
