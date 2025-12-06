from datetime import date

def calculate_priority_score(obj, today=None):
    """
    Формула из ТЗ:
    PriorityScore = (6 - состояние) * 3 + возраст паспорта в годах
    """

    if today is None:
        today = date.today()

    # возраст паспорта
    age_years = today.year - obj.passport_date.year
    if (today.month, today.day) < (obj.passport_date.month, obj.passport_date.day):
        age_years -= 1

    # техническое состояние (1–5) → чем больше → хуже
    tech = obj.technical_condition

    score = (6 - tech) * 3 + age_years
    return max(score, 0)
