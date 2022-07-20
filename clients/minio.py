import asyncio
import os

from aiobotocore.session import get_session

AWS_ACCESS_KEY_ID = "xxx"
AWS_SECRET_ACCESS_KEY = "xxx"


async def go():
    bucket = "telegram"
    filename = "test.txt"
    folder = "aiobotocore"
    key = "{}/{}".format(folder, filename)

    session = get_session()
    async with session.create_client(
        "s3",
        region_name="",
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
    ) as client:
        # upload object to amazon s3
        data = b"\x01" * 1024
        resp = await client.put_object(Bucket=bucket, Key=key, Body=data)
        print(resp)

        # getting s3 object properties of file we just uploaded
        resp = await client.get_object_acl(Bucket=bucket, Key=key)
        print(resp)

        # get object from s3
        response = await client.get_object(Bucket=bucket, Key=key)
        # this will ensure the connection is correctly re-used/closed
        async with response["Body"] as stream:
            assert await stream.read() == data

        # list s3 objects using paginator
        paginator = client.get_paginator("list_objects")
        async for result in paginator.paginate(Bucket=bucket, Prefix=folder):
            for c in result.get("Contents", []):
                print(c)

        # delete object from s3
        resp = await client.delete_object(Bucket=bucket, Key=key)
        print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(go())
