from django.db import models
from Users.models import *
from django.utils.timezone import now


class Tasks(models.Model):

    Type=(
        ("1", "Individual"),
        ("2", "Group"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    mode = models.CharField(max_length=20, choices = Type, default = "1")
    reward = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=now, editable = False)
    updated_at = models.DateTimeField(default=now, editable = False)
    pass

class Task_submission(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    task_id = models.ForeignKey(Tasks, on_delete=models.PROTECT)
    sumbission_time = models.DateTimeField(auto_now_add=True, editable=False)

    pass
# Create your models here.
