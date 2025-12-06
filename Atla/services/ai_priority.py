import requests
from django.conf import settings

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
OPENROUTER_MODEL = "kwaipilot/kat-coder-pro:free"   # лёгкая и дешёвая, хватит с головой

def analyze_object_with_ai(obj, score):
    """
    Отправляет данные объекта в ИИ и получает вероятность риска (0–1).
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
    Ты — модель оценки технического риска объекта инфраструктуры.

    Данные объекта:
    Название: {obj.name}
    Регион: {obj.region}
    Тип ресурса: {obj.resource_type}
    Тип воды: {obj.water_type}
    Фауна: {obj.fauna}
    Состояние: {obj.technical_condition}
    Возраст паспорта: {obj.passport_date}
    Приоритетное значение (score): {score}

    Дай ответ строго в JSON:
    {{
      "risk_prob": <число от 0 до 1>,
      "explanation": "<коротко почему>"
    }}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    response = requests.post(url, json=data, headers=headers, timeout=30)
    response.raise_for_status()

    raw = response.json()["choices"][0]["message"]["content"]

    # Пытаемся распарсить JSON от модели
    import json
    try:
        parsed = json.loads(raw)
        return parsed["risk_prob"], parsed["explanation"]
    except Exception:
        # fallback — если модель дала текст вместо JSON
        return None, raw