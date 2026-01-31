# TODO: SleepLog 모델을 작성해 보세요.
# 힌트: sleep_date, start_time, end_time, quality 필드가 필요합니다.
from tortoise import fields, models

class SleepLog(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="sleep_logs")
    # 실제 날짜/시간 필드로 선언
    sleep_date = fields.DateField()    
    start_time = fields.DatetimeField()    
    end_time = fields.DatetimeField()    
    quality = fields.IntField(null=True) 

    def __str__(self) -> str:
        return f"{self.user_id} - {self.quality} ({self.quality})"