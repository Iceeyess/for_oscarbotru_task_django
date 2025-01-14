from django.contrib import admin

from notifications.models import Notification, LogInfo


# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'recipient', 'delay', 'next_send', 'type', )
    list_display_links = ('id', 'message', 'recipient', 'delay', 'next_send', 'type', )
    filter_display_links = ('id', 'message', 'recipient', )


@admin.register(LogInfo)
class LogInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'code')
    list_display_links = ('id', 'status', 'code')
    filter_display_links = ('id', 'status', 'code', )
