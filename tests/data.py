from tests.clients.tg import data
from tests.clients.fapi import data as fapi_data

GET_UPDATES = {
    "ok": True,
    "result": [
        {
            "update_id": 503972235,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 85364161,
                    "is_bot": False,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "language_code": "en",
                },
                "chat": {
                    "id": 85364161,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "type": "private",
                },
                "date": 1634815235,
                "text": "/start",
                "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
            },
        }
    ],
}

GET_EMPTY_UPDATES = {"ok": True, "result": []}
GET_OFFSET_UPDATES = {
    "ok": True,
    "result": [
        {
            "update_id": 503972236,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 85364161,
                    "is_bot": False,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "language_code": "en",
                },
                "chat": {
                    "id": 85364161,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "type": "private",
                },
                "date": 1634815235,
                "text": "hello",
                "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
            },
        }
    ],
}
SEND_MESSAGE = data.SEND_MESSAGE

GET_UPDATES_WITH_DOCUMENT = {
    "ok": True,
    "result": [
        {
            "update_id": 503972289,
            "message": {
                "message_id": 132,
                "from": {
                    "id": 85364161,
                    "is_bot": False,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "language_code": "en",
                },
                "chat": {
                    "id": 85364161,
                    "first_name": "Alexander",
                    "last_name": "Opryshko",
                    "username": "alexopryshko",
                    "type": "private",
                },
                "date": 1635672833,
                "document": {
                    "file_name": "Памятка наставника_KTS.pdf",
                    "mime_type": "application/pdf",
                    "thumb": {
                        "file_id": "file_id",
                        "file_unique_id": "file_unique_id",
                        "file_size": 10536,
                        "width": 226,
                        "height": 320,
                    },
                    "file_id": "file_id",
                    "file_unique_id": "file_unique_id",
                    "file_size": 84011,
                },
            },
        }
    ],
}
GET_FILE = fapi_data.GET_FILE
