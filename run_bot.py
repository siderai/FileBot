import asyncio
import os

from bot import Bot, BotConfig, WorkerConfig

# should be set in Env, here is testing sample
os.environ["BOT_TOKEN"] = "5289616541:AAH8ECV8trIJzVu9PJkm4IM2Gz7eCkeUtf4"


def run():
    loop = asyncio.get_event_loop()

    worker_config = WorkerConfig(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        bucket="telegram",
        concurrent_workers=2,
    )
    bot_config = BotConfig(token=os.getenv("BOT_TOKEN"), worker=worker_config)
    tg_bot = Bot(bot_config)

    try:
        print("bot has been started")
        loop.create_task(tg_bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping bot")
        loop.run_until_complete(tg_bot.stop())


if __name__ == "__main__":
    run()
