from django.urls import path

from notifications.apps import NotificationsConfig
from notifications import views


app_name = NotificationsConfig.name

urlpatterns = [
    path('api/notify/', views.NotificationAPI.as_view(), name='notification'),
]


