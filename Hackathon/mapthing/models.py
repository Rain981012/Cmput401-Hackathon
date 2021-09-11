from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User


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

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.event_name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'startTime': self.start_date.timestamp(),
            'endTime': self.end_date.timestamp(),
            'public': self.public,
            'creator': str(self.creator.id)
        }
        if self.min_number_people is not None:
            data['minPeople'] = self.min_number_people
            data['maxPeople'] = self.max_number_people
        return data


class Attend(models.Model):
    attendee = models.ForeignKey(User, on_delete=CASCADE)
    associated_event = models.ForeignKey(Event, on_delete=CASCADE)
