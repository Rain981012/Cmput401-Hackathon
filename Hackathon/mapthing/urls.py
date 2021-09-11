from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/create-user/', views.create_user, name='create-user'),
    path('api/create-event/', views.create_event, name='create-event'),
]
