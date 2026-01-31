from datetime import date, datetime
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.models.water import WaterLog
from app.models.exercise import ExerciseLog     #=======모델 만든거 임포트해주기
from app.models.meal import MealLog
from app.models.sleep import SleepLog

from app.services.mock_data import (
    add_exercise,
    add_meal,
    add_sleep,
    delete_exercise,
    delete_meal,
    delete_sleep,
    list_exercise,
    list_meal,
    list_sleep,
    update_exercise,
    update_meal,
    update_sleep,
)
from app.services.users import get_or_create_default_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def build_water_report(logs: list[WaterLog], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not logs:
        plt.figure(figsize=(7, 3.5))
        plt.text(0.5, 0.5, "데이터 없음", ha="center", va="center", fontsize=12)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=140)
        plt.close()
        return

    rows = [{"date": log.logged_at.date(), "amount_ml": log.amount_ml} for log in logs]
    df = pd.DataFrame(rows)
    daily = df.groupby("date", as_index=False)["amount_ml"].sum()

    plt.figure(figsize=(7, 3.5))
    plt.bar(daily["date"].astype(str), daily["amount_ml"], color="#6e7bff")
    plt.title("일별 수분 섭취량")
    plt.ylabel("ml")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


@router.get("/")        #==================================추가
async def dashboard(request: Request):
    user = await get_or_create_default_user()
    water_logs = await WaterLog.filter(user=user).order_by("-logged_at").limit(5)
    exercise_logs = await ExerciseLog.filter(user=user).order_by("-logged_at").limit(5)
    sleep_logs = await SleepLog.filter(user=user).order_by("-sleep_date", "-start_time").limit(5)
    meal_logs = await MealLog.filter(user=user).order_by("-eaten_at").limit(5)

    return templates.TemplateResponse(      #++++++++++++++++++++++++++++++++++++++++++++++수정 ORM방식으로
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "water_logs": water_logs,
            "exercise_logs": exercise_logs,
            "sleep_logs": sleep_logs,
            "meal_logs": meal_logs,
        },
    )

#++++++++++++이거 참고 겟메소드=============
@router.get("/water")
async def water_page(request: Request):
    user = await get_or_create_default_user()
    logs = await WaterLog.filter(user=user).order_by("-logged_at")
    return templates.TemplateResponse(
        "water.html", {"request": request, "user": user, "logs": logs}
    )


@router.post("/water")
async def add_water(amount_ml: int = Form(...)):
    user = await get_or_create_default_user()
    await WaterLog.create(user=user, amount_ml=amount_ml)
    return RedirectResponse(url="/water", status_code=303)


@router.post("/water/{log_id}/edit")
async def edit_water(
    log_id: int, amount_ml: int = Form(...), logged_at: str = Form(...)
):
    user = await get_or_create_default_user()
    log = await WaterLog.get_or_none(id=log_id, user=user)
    if log:
        log.amount_ml = amount_ml
        log.logged_at = datetime.fromisoformat(logged_at)
        await log.save(update_fields=["amount_ml", "logged_at"])
    return RedirectResponse(url="/water", status_code=303)


@router.post("/water/{log_id}/delete")
async def delete_water(log_id: int):
    user = await get_or_create_default_user()
    log = await WaterLog.get_or_none(id=log_id, user=user)
    if log:
        await log.delete()
    return RedirectResponse(url="/water", status_code=303)

# 1. .get("/exercise") water처럼 수정함============================================1
@router.get("/exercise")
async def exercise_page(request: Request):
    user = await get_or_create_default_user()
    logs = await ExerciseLog.filter(user=user).order_by("-logged_at")
    return templates.TemplateResponse(
        "exercise.html", {"request": request, "user": user, "logs": logs}
    )

@router.post("/exercise")
async def add_exercise_log(
    activity: str = Form(...),
    duration_min: int = Form(...),
    calories_burned: int | None = Form(None),
):
    # TODO: ORM 모델과 테이블로 교체하세요. 2.................ORM모델 테이블 
    user = await get_or_create_default_user()
    await ExerciseLog.create(
        user=user,
        activity=activity,
        duration_min=duration_min,
        calories_burned=calories_burned )
    return RedirectResponse(url="/exercise", status_code=303)


@router.post("/exercise/{log_id}/edit")
async def edit_exercise_log(
    log_id: int,
    activity: str = Form(...),
    duration_min: int = Form(...),
    calories_burned: int | None = Form(None),
    logged_at: str = Form(...),
):
    # TODO: ORM 모델과 테이블로 교체하세요.--FastAPI + Tortoise에서는 DB 작업 모두 async(await → 비동기 함수 호출 -----3
    user = await get_or_create_default_user()   #조건
    log = await ExerciseLog.get_or_none(id=log_id, user=user) #(ExerciseLog)을 DB에서 찾는다.
    if log:                 #.get_or_none() → 있으면 모델 객체 반환, 없으면 None
        log.activity = activity
        log.duration_min = duration_min
        log.calories_burned = calories_burned or 0
        log.logged_at = datetime.fromisoformat(logged_at)
        await log.save(update_fields=["activity", "duration_min", "calories_burned", "logged_at"])  #수정된 필드만 DB에 업데이트
    return RedirectResponse(url="/exercise", status_code=303)   #저장 후 /exercise 페이지로 리다이렉트


@router.post("/exercise/{log_id}/delete")
async def delete_exercise_log(log_id: int):
    # TODO: ORM 모델과 테이블로 교체하세요.-----------------------4
    user = await get_or_create_default_user()
    log = await ExerciseLog.get_or_none(id=log_id, user=user)
    if log:
        await log.delete()
    return RedirectResponse(url="/exercise", status_code=303)


# . .get("/sleep") water처럼 수정함============================================마지막
@router.get("/sleep")
async def sleep_page(request: Request):
    user = await get_or_create_default_user()
    logs = await SleepLog.filter(user=user).order_by("-sleep_date", "-start_time") #최근 날짜부터 정렬
    return templates.TemplateResponse(
        "sleep.html",
        {"request": request, "user": user, "logs": logs}
    )


@router.post("/sleep")
async def add_sleep_log(
    sleep_date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    quality: int | None = Form(None),
):
    # TODO: ORM 모델과 테이블로 교체하세요.===========================
    user = await get_or_create_default_user()
    sleep_date_dt = date.fromisoformat(sleep_date)
    start_time_dt = datetime.fromisoformat(start_time)
    end_time_dt = datetime.fromisoformat(end_time)

    await SleepLog.create(user=user, 
        sleep_date=sleep_date_dt,
        start_time=start_time_dt,
        end_time=end_time_dt,
        quality=quality
    )
    return RedirectResponse(url="/sleep", status_code=303)



@router.post("/sleep/{log_id}/edit")
async def edit_sleep_log(
    log_id: int,
    sleep_date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    quality: int | None = Form(None),
):
    # TODO: ORM 모델과 테이블로 교체하세요.==========================================
    user = await get_or_create_default_user()
    log = await SleepLog.get_or_none(id=log_id, user=user)
    if log:
        log.sleep_date=date.fromisoformat(sleep_date)
        log.start_time=datetime.fromisoformat(start_time)
        log.end_time=datetime.fromisoformat(end_time)
        log.quality=quality
        await log.save(update_fields=["sleep_date", "start_time","end_time","quality"])
    return RedirectResponse(url="/sleep", status_code=303)


@router.post("/sleep/{log_id}/delete")
async def delete_sleep_log(log_id: int):
    # TODO: ORM 모델과 테이블로 교체하세요.
    user = await get_or_create_default_user()
    log = await SleepLog.get_or_none(id=log_id, user=user)
    if log:
        await log.delete()
    return RedirectResponse(url="/sleep", status_code=303)



#==========================================================5. meal 가져오기============
@router.get("/meal")
async def meal_page(request: Request):
    user = await get_or_create_default_user()
    logs = await MealLog.filter(user=user).order_by("-eaten_at")
    return templates.TemplateResponse(
        "meal.html",{"request": request, "user": user, "logs": logs}
    )


@router.post("/meal")
async def add_meal_log(
    meal_type: str = Form(...),
    calories: int | None = Form(None),
    note: str | None = Form(None),
    eaten_at: str = Form(...),
):
    # TODO: ORM 모델과 테이블로 교체하세요.-----------------------------6
    user = await get_or_create_default_user()
    eaten_at_dt = datetime.fromisoformat(eaten_at)  #문자열 eaten_at → datetime 변환

    await MealLog.create(
        user=user,
        meal_type = meal_type,
        calories = calories,
        note = note,
        eaten_at = eaten_at_dt)
    return RedirectResponse(url="/meal",status_code=303)


#    add_meal(meal_type, calories, note)
#    return RedirectResponse(url="/meal", status_code=303)


@router.post("/meal/{log_id}/edit")
async def edit_meal_log(
    log_id: int,
    meal_type: str = Form(...),
    calories: int | None = Form(None),
    note: str | None = Form(None),
    eaten_at: str = Form(...),
):
    # TODO: ORM 모델과 테이블로 교체하세요.===========================================
    user = await get_or_create_default_user()
    log = await MealLog.get_or_none(id=log_id, user=user) #(MealLog)을 DB에서 찾는다.
    if log:                 #.get_or_none() → 있으면 모델 객체 반환, 없으면 None
        log.meal_type = meal_type
        log.calories = calories
        log.note = note
        log.eaten_at = datetime.fromisoformat(eaten_at)
        await log.save(update_fields=["meal_type", "calories", "note", "eaten_at"])  #수정된 필드만 DB에 업데이트
    return RedirectResponse(url="/meal", status_code=303)   #저장 후 /meal 페이지로 리다이렉트


#    update_meal(log_id, meal_type, calories, note, datetime.fromisoformat(eaten_at))
#    return RedirectResponse(url="/meal", status_code=303)


@router.post("/meal/{log_id}/delete")
async def delete_meal_log(log_id: int):
    # TODO: ORM 모델과 테이블로 교체하세요.-----------------------------------
    user = await get_or_create_default_user()
    log = await MealLog.get_or_none(id=log_id, user=user)
    if log:
        await log.delete()
    return RedirectResponse(url="/meal", status_code=303)


@router.get("/report")
async def report_page(request: Request):
    user = await get_or_create_default_user()
    logs = await WaterLog.filter(user=user).order_by("logged_at")
    output_path = Path("app/static/img/water_report.png")
    build_water_report(logs, output_path)
    total_water = sum(log.amount_ml for log in logs)
    days = len({log.logged_at.date() for log in logs})
    avg_per_day = round(total_water / days, 1) if days else 0

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "user": user,
            "chart_url": "/static/img/water_report.png",
            "total_water": total_water,
            "days": days,
            "avg_per_day": avg_per_day,
        },
    )
