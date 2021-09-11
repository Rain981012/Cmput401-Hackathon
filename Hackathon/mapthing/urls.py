from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/create-user/', views.create_user, name='create-user'),
    path('api/create-event/', views.create_event, name='create-event'),
    path('api/attend-event/', views.attend_event, name='attend-event'),
    path('api/event/<str:event_id>/', views.event, name='event'),
    path('api/get-events/', views.get_events, name='get-event')
]
