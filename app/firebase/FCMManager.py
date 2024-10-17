import base64
import json
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError
from fastapi import Response, status
from ..config import settings

raw_creds = json.loads(settings.firebase.credentials)
raw_creds["private_key"] = raw_creds["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(raw_creds)
firebase_admin.initialize_app(cred)


def sendPush(title: str, msg: str, registration_tokens: list[str], dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=msg),
        data=dataObject if dataObject is not None else {},
        tokens=registration_tokens,
    )

    try:
        request = messaging.send_each_for_multicast(multicast_message=message, dry_run=False)
    except ValueError:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Неверный формат данных.",
        )
    except FirebaseError:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Ошибка в отправке уведомления.",
        )

    return Response(
        status_code=status.HTTP_200_OK,
        content="Пуш-уведомление успешно отправлено.",
    )
