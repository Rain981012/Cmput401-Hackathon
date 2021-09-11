from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    creator = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    longitude = models.FloatField()
    latitude = models.FloatField()
    start_date = models.DateTimeField('published date')
    end_date = models.DateTimeField('end date')
    attendants = models.IntegerField(default=0)
    visibility = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.event_name