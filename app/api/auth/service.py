from fastapi import HTTPException, status
import httpx
from app.config import settings


def get_verification_code_via_flashcall(phone_number_to_call: int, public_key: str, campaign_id: int):
    with httpx.Client() as client:
        form_data = {
            "public_key": public_key,
            "phone": "+7" + phone_number_to_call,
            "campaign_id": campaign_id,
        }
        request = client.post(
            "https://zvonok.com/manager/cabapi_external/api/v1/phones/flashcall/",
            data=form_data,
        )
    return request


def get_verification_code(phone_number: str):
    verification_code_request = get_verification_code_via_flashcall(
        phone_number_to_call=phone_number,
        public_key=settings.flashcall.public_key,
        campaign_id=settings.flashcall.campaign_id,
    )
    response_status_code = verification_code_request.status_code
    if response_status_code == 200:
        verification_code = verification_code_request.json()["data"]["pincode"]
    elif response_status_code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный номер телефона.")
    elif response_status_code == 429:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Слишком много запросов.")
    elif response_status_code == 503:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Попробуйте чуть позже, в данный момент сервис звонков перегружен.",
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return verification_code
