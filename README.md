# Telegram File Bot

Saves your files to cloud storage Minio (S3).

Performs well even with large files thanks to the data streaming protocol. Limit: up to 2gb each file.

In order to start, you need to define environment variables:
```
"BOT_TOKEN"
"MINIO_SERVER_URL"
"MINIO_ROOT_PASSWORD"
"MINIO_ROOT_USER" 
```

Then execute run_bot.py
