# TODO: ExerciseLog 모델을 작성해 보세요.
# 힌트: activity, duration_min, calories_burned, logged_at 필드가 필요합니다.

from dataclasses import field
from tortoise import fields, models


class ExerciseLog(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="exercise_logs")
    activity = fields.CharField(max_length=100)
    duration_min = fields.IntField()
    calories_burned = fields.IntField()
    logged_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.duration_min}분"
