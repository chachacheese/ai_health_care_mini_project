# TODO: MealLog 모델을 작성해 보세요.
# 힌트: meal_type, calories, note, eaten_at 필드가 필요합니다.
from tortoise import fields, models

class MealLog(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="meal_logs")
    meal_type = fields.CharField(max_length=100)
    calories = fields.IntField(null=True)  # 폼에서 None 가능하면 null=True 추천
    note = fields.CharField(max_length=200, null=True)  # None 가능하면 null=True 추천
    eaten_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.meal_type} ({self.calories or 0}kcal)"