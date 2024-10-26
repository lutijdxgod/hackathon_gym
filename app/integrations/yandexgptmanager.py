import httpx
from ..config import settings


def generate_prompt(message: str) -> dict:
    prompt = {
        "modelUri": settings.yandexgpt.uri,
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": "Ты - самый опытный тренер по бодибилдингу/фитнесу/пауэрлифтингу."},
            {"role": "user", "text": message},
        ],
    }
    return prompt


def get_exercise_advice(exercise_name: str, equipment_name: str):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.yandexgpt.iam_token}"}
    with httpx.Client() as client:
        request = client.post(
            url=settings.yandexgpt.url,
            headers=headers,
            json=generate_prompt(
                message=f"Привет! Мне нужна твоя помощь, чтобы узнать больше о том, как выполнять следующее упражнение - <{exercise_name}> на тренажёре <{equipment_name}>",
            ),
        )
    return request.json()["result"]["alternatives"][0]["message"]["text"]
