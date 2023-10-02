from django.db import models
from uuid import uuid4

# Create your models here.

class Video(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='videos/')
    url = models.URLField(null=True)
    transcription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name
