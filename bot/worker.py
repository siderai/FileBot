import asyncio
from dataclasses import dataclass
from typing import List

from clients.tg.api import TgClient
from clients.fapi.s3 import S3Client
from clients.tg.dcs import UpdateObj, Message, Chat, Document
from bot.utils import log_exceptions


@dataclass
class WorkerConfig:
    endpoint_url: str
    aws_secret_access_key: str
    aws_access_key_id: str
    bucket: str
    concurrent_workers: int = 1


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, config: WorkerConfig):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.config = config
        self.s3 = S3Client(
            endpoint_url=config.endpoint_url,
            aws_secret_access_key=config.aws_secret_access_key,
            aws_access_key_id=config.aws_access_key_id,
        )
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, update: UpdateObj):
        """
        в этом методе происходит обработка сообщений и реализация бизнес-логики
        """
        # send greeting message
        chat_id = update.message.chat.id
        # await self.tg_client.send_message(chat_id, text='[greeting]')
        # if update.message.message_id == 1:
        #     await self.tg_client.send_message(chat_id, text='[greeting]')

        # Реагирует только на документы. Если в сообщении нет документа, просит добавить
        doc = update.message.document
        if not doc:
            await self.tg_client.send_message(chat_id, text="[document is required]")
            return

        # Подтверждает загрузку файла в тг
        await self.tg_client.send_message(chat_id, text="[document]")

        # Если размер файла более 100 мб - стримит чанками по S3, если менее - загружает целиком
        if doc.file_size > 100 * 1024:
            await self.s3.stream_upload(
                bucket=self.config.bucket,
                path=f"/{doc.file_name}",
                # ссылка на скачивание файла из тг
                url=f"https://api.telegram.org/file/bot{self.tg_client.token}/{doc.file_id}",
            )

            await self.tg_client.send_message(chat_id, text="[document has been saved]")

        else:
            await self.s3.fetch_and_upload(
                bucket=self.config.bucket,
                path=f"/{doc.file_name}",
                url=f"https://api.telegram.org/file/bot{self.tg_client.token}/{doc.file_id}",
            )

            await self.tg_client.send_message(chat_id, text="[document has been saved]")

    async def _worker(self):
        """
        должен получать сообщения из очереди и вызывать handle_update
        """
        while True:
            update: UpdateObj = await self.queue.get()
            await self.handle_update(update)
            self.queue.task_done()

    def start(self):
        """
        должен запустить столько воркеров, сколько указано в config.concurrent_workers
        запущенные задачи нужно положить в _tasks
        """
        for _ in range(self.config.concurrent_workers):
            task = asyncio.create_task(self._worker())
            self._tasks.append(task)

    async def stop(self):
        """
        нужно дождаться пока очередь не станет пустой (метод join у очереди), а потом отменить все воркеры
        """
        await self.queue.join()
        for task in self._tasks:
            task.cancel()
        await asyncio.wait(self._tasks, return_when=asyncio.ALL_COMPLETED)
