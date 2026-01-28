from datetime import date, datetime

# TODO: 아래 in-memory 데이터는 ORM으로 교체하는 과제입니다.

_exercise_id = 2
_sleep_id = 1
_meal_id = 1

_exercise_logs = [
    {
        "id": 1,
        "activity": "러닝",
        "duration_min": 30,
        "calories_burned": 260,
        "logged_at": datetime.now(),
    },
    {
        "id": 2,
        "activity": "요가",
        "duration_min": 45,
        "calories_burned": 180,
        "logged_at": datetime.now(),
    },
]

_sleep_logs = [
    {
        "id": 1,
        "sleep_date": date.today(),
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "quality": 4,
    }
]

_meal_logs = [
    {
        "id": 1,
        "meal_type": "아침",
        "calories": 420,
        "note": "그릭요거트",
        "eaten_at": datetime.now(),
    }
]


def list_exercise():
    return _exercise_logs


def add_exercise(activity: str, duration_min: int, calories_burned: int | None):
    global _exercise_id
    _exercise_id += 1
    _exercise_logs.insert(
        0,
        {
            "id": _exercise_id,
            "activity": activity,
            "duration_min": duration_min,
            "calories_burned": calories_burned,
            "logged_at": datetime.now(),
        },
    )


def update_exercise(
    log_id: int,
    activity: str,
    duration_min: int,
    calories_burned: int | None,
    logged_at: datetime,
):
    for log in _exercise_logs:
        if log["id"] == log_id:
            log["activity"] = activity
            log["duration_min"] = duration_min
            log["calories_burned"] = calories_burned
            log["logged_at"] = logged_at
            return True
    return False


def delete_exercise(log_id: int):
    for idx, log in enumerate(_exercise_logs):
        if log["id"] == log_id:
            _exercise_logs.pop(idx)
            return True
    return False


def list_sleep():
    return _sleep_logs


def add_sleep(sleep_date: date, start_time: datetime, end_time: datetime, quality: int | None):
    global _sleep_id
    _sleep_id += 1
    _sleep_logs.insert(
        0,
        {
            "id": _sleep_id,
            "sleep_date": sleep_date,
            "start_time": start_time,
            "end_time": end_time,
            "quality": quality,
        },
    )


def update_sleep(
    log_id: int, sleep_date: date, start_time: datetime, end_time: datetime, quality: int | None
):
    for log in _sleep_logs:
        if log["id"] == log_id:
            log["sleep_date"] = sleep_date
            log["start_time"] = start_time
            log["end_time"] = end_time
            log["quality"] = quality
            return True
    return False


def delete_sleep(log_id: int):
    for idx, log in enumerate(_sleep_logs):
        if log["id"] == log_id:
            _sleep_logs.pop(idx)
            return True
    return False


def list_meal():
    return _meal_logs


def add_meal(meal_type: str, calories: int | None, note: str | None):
    global _meal_id
    _meal_id += 1
    _meal_logs.insert(
        0,
        {
            "id": _meal_id,
            "meal_type": meal_type,
            "calories": calories,
            "note": note,
            "eaten_at": datetime.now(),
        },
    )


def update_meal(
    log_id: int, meal_type: str, calories: int | None, note: str | None, eaten_at: datetime
):
    for log in _meal_logs:
        if log["id"] == log_id:
            log["meal_type"] = meal_type
            log["calories"] = calories
            log["note"] = note
            log["eaten_at"] = eaten_at
            return True
    return False


def delete_meal(log_id: int):
    for idx, log in enumerate(_meal_logs):
        if log["id"] == log_id:
            _meal_logs.pop(idx)
            return True
    return False
