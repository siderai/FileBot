import asyncio

from aioresponses import aioresponses, CallbackResult

from bot.poller import Poller
from clients.tg.dcs import UpdateObj

from . import data


class TestPoller:
    async def test_queue(self, tg_token, tg_base_url):
        q = asyncio.Queue()
        with aioresponses() as m:
            m.get(tg_base_url(f'getUpdates?timeout=60'), payload=data.GET_UPDATES)
            m.get(tg_base_url(f'getUpdates?offset=503972236&timeout=60'), payload=data.GET_OFFSET_UPDATES)

            async def callback(*_, **__):
                await asyncio.sleep(10)
                return CallbackResult(payload=data.GET_EMPTY_UPDATES)

            m.get(tg_base_url(f'getUpdates?offset=503972237&timeout=60'), callback=callback)
            poller = Poller(tg_token, q)
            poller.start()
            await asyncio.sleep(0)

            upd: UpdateObj = await asyncio.wait_for(q.get(), timeout=1)
            assert upd.update_id == data.GET_UPDATES['result'][0]['update_id']

            upd: UpdateObj = await asyncio.wait_for(q.get(), timeout=1)
            assert upd.update_id == data.GET_OFFSET_UPDATES['result'][0]['update_id']

            await poller.stop()

    async def test_stop(self, tg_token):
        q = asyncio.Queue()
        poller = Poller(tg_token, q)
        poller.start()
        await asyncio.sleep(0)

        assert poller._task._state == 'PENDING'
        await poller.stop()
        assert poller._task._state == 'CANCELLED'
