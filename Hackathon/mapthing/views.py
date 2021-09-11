from datetime import datetime
from json.encoder import JSONEncoder
from django.db.models.deletion import RestrictedError
from django.utils import timezone
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.contrib.auth.models import User
from .models import Event, Attend

from .util import get, require


def index(request):
    return HttpResponse('This is the index page.')


def create_event(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'invalid request'})

    try:
        event_data = require(request.POST, 'event', QueryDict)
        name = require(event_data, 'name', str)
        description = require(event_data, 'description', str)
        latitude = require(event_data, 'latitude', float)
        longitude = require(event_data, 'longitude', float)
        start_time = datetime.fromtimestamp(
            require(event_data, 'startTime', float))
        end_time = datetime.fromtimestamp(
            require(event_data, 'endTime', float))
        min_people = get(event_data, 'minPeople')
        max_people = get(event_data, 'maxPeople')
    except (KeyError, TypeError, ValueError) as e:
        return JsonResponse({'success': False, 'error': e.args[0]})

    event = Event(event_name=name,
                  creator=request.user,
                  description=description,
                  latitude=latitude,
                  longitude=longitude,
                  start_date=start_time,
                  end_date=end_time,
                  min_number_people=min_people,
                  max_number_people=max_people)
    event.save()
    return JsonResponse({'success': True, 'eventId': event.id})


def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'invalid request'})

    try:
        name = require(request.POST, 'name', str)
    except (KeyError, TypeError) as e:
        return JsonResponse({'success': False, 'error': e.args[0]})

    user = User.objects.create_user(name)
    return JsonResponse({'success': True, 'userId': user.id})


def attend_event(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'invalid request'})
    try:
        eventID = require(request.POST, 'eventId', str)
        event = Event.objects.get(id=eventID)
        attendee = request.user
        attend = Attend(attendee, event)
        attend.save()
        if event.exists() == True:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    except (KeyError, TypeError) as e:
        return JsonResponse({'success': False, 'error': e.args[0]})


def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'event does not exist'})
    return JsonResponse(event.serialize())

def get_events(request):
    if request.method == 'GET':
        result = Event.objects.all().filter(end_date__gte=timezone.now())
        events = list(map(Event.serialize, result))
        return JsonResponse({'events': events})