import logging


async def log_exceptions(awaitable):
    try:
        return await awaitable
    except Exception as e:
        logging.exception(e)
