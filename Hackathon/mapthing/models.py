from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

class User(models.Model):
    user_name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.user_name

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=CASCADE)
    description = models.CharField(max_length=400)
    longitude = models.FloatField()
    latitude = models.FloatField()
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    min_number_people = models.IntegerField(null=True)
    max_number_people = models.IntegerField(null=True)
    public = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.event_name
    
class Attend(models.Model):
    attendee = models.ForeignKey(User, on_delete=CASCADE)
    associated_event = models.ForeignKey(Event, on_delete=CASCADE)