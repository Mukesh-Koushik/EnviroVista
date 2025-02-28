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

    def __str__(self):
        return self.name
    pass

class Task_submission(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    task_id = models.ForeignKey(Tasks, on_delete=models.PROTECT)
    sumbission_time = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to='task_submissions/', blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user_id.username} - {self.task_id.name}"
# Create your models here.

class MediaMetadata(models.Model):
    file = models.FileField(upload_to="uploads/")
    filename = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metadata for {self.file.name}"
    
class IdeaForge(models.Model):
    task_name = models.CharField(max_length= 30, blank=True)
    task_description = models.TextField()
    task_video = models.FileField(upload_to='Ideaforge_submissions/', blank=True)