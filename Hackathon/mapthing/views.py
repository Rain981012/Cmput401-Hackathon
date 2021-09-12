from datetime import datetime
from json.encoder import JSONEncoder
from django.db.models.deletion import RestrictedError
from django.middleware import csrf
from django.utils import timezone
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Attend

from .util import get, require

import json


@csrf_exempt
def index(request):
    return HttpResponse('This is the index page.')


@csrf_exempt
def create_event(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'invalid request'})

    try:
        req_data = json.loads(request.body)
        event_data = require(req_data, 'event')
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
                  creator_name=request.user,
                  description=description,
                  latitude=latitude,
                  longitude=longitude,
                  start_date=start_time,
                  end_date=end_time,
                  min_number_people=min_people,
                  max_number_people=max_people)
    event.save()
    return JsonResponse({'success': True, 'eventId': event.id})


@csrf_exempt
def attend_event(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'invalid request'})
    try:
        req_data = json.loads(request.body)
        eventID = require(req_data, 'eventId', str)
        event = Event.objects.get(id=eventID)
        attendee_name = require(req_data, 'attendeeName', str)
        attend = Attend(attendee_name=attendee_name, associated_event=event)
        attend.save()
        if event.exists() == True:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    except (KeyError, TypeError) as e:
        return JsonResponse({'success': False, 'error': e.args[0]})


@csrf_exempt
def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'event does not exist'})
    return JsonResponse(event.serialize())


@csrf_exempt
def get_events(request):
    if request.method == 'GET':
        result = Event.objects.all().filter(end_date__gte=timezone.now())
        events = list(map(Event.serialize, result))
        return JsonResponse({'events': events})
