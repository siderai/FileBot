import asyncio
from unittest.mock import patch

from aioresponses import aioresponses, CallbackResult

from bot import WorkerConfig
from bot.worker import Worker
from clients.fapi.s3 import S3Client
from . import data


class TestWorker:
    async def test_queue(self, tg_token, tg_base_url, worker_config, update_obj):
        q = asyncio.Queue()
        worker = Worker(tg_token, q, worker_config)
        q.put_nowait(update_obj)

        def callback(*_, json, **__):
            assert 'chat_id' in json
            assert 'text' in json
            return CallbackResult(payload=data.SEND_MESSAGE)

        with aioresponses() as m:
            m.post(tg_base_url('sendMessage'), callback=callback)
            worker.start()

            try:
                await asyncio.wait_for(worker.stop(), 1)
            except asyncio.TimeoutError:
                assert False, 'probably exception has been accrued and queue.task_done() has not been called'

        assert q.empty()

    async def test_stop(self, tg_token, worker_config: WorkerConfig):
        q = asyncio.Queue()
        worker = Worker(tg_token, q, worker_config)
        worker.start()

        await asyncio.sleep(0)
        assert len(worker._tasks) == worker_config.concurrent_workers
        assert all([t._state == 'PENDING' for t in worker._tasks])

        await worker.stop()
        assert all([t._state == 'CANCELLED' for t in worker._tasks])


class TestHandler:
    async def test_first_message(self, tg_worker, update_obj, tg_base_url):
        q = asyncio.Queue()
        worker = tg_worker(q)

        def callback(*_, json, **__):
            assert 'chat_id' in json
            assert 'text' in json
            text = json['text']
            assert '[greeting]' in text
            return CallbackResult(payload=data.SEND_MESSAGE)

        with aioresponses() as m:
            m.post(tg_base_url('sendMessage'), callback=callback)
            await worker.handle_update(update_obj)

    async def test_second_message(self, tg_worker, update_obj, tg_base_url):
        q = asyncio.Queue()
        worker = tg_worker(q)

        def callback(*_, json, **__):
            assert 'chat_id' in json
            assert 'text' in json
            text = json['text']
            assert '[document is required]' in text
            return CallbackResult(payload=data.SEND_MESSAGE)

        with aioresponses() as m:
            m.post(tg_base_url('sendMessage'), payload=data.SEND_MESSAGE)
            m.post(tg_base_url('sendMessage'), callback=callback)
            await worker.handle_update(update_obj)
            await worker.handle_update(update_obj)

    async def test_document(
        self, tg_worker, update_obj, update_obj_with_document,
        tg_base_url, tg_api_url, tg_token,
    ):
        q = asyncio.Queue()
        worker = tg_worker(q)

        def callback1(*_, json, **__):
            text = json['text']
            assert '[document]' in text
            return CallbackResult(payload=data.SEND_MESSAGE)

        def callback2(*_, json, **__):
            text = json['text']
            assert '[document has been saved]' in text
            return CallbackResult(payload=data.SEND_MESSAGE)

        with aioresponses() as m:
            m.post(tg_base_url('sendMessage'), payload=data.SEND_MESSAGE)
            m.post(tg_base_url('sendMessage'), callback=callback1)
            m.get(tg_base_url('getFile?file_id=file_id'), payload=data.GET_FILE)
            file_path = data.GET_FILE['result']['file_path']
            m.get(f'{tg_api_url}/file/bot{tg_token}/{file_path}', content_type='text/plain', body=b'body')
            m.post(tg_base_url('sendMessage'), callback=callback2)

            with patch.object(S3Client, 'fetch_and_upload', return_value=None):
                with patch.object(S3Client, 'stream_upload', return_value=None):
                    await worker.handle_update(update_obj)
                    await worker.handle_update(update_obj_with_document)
