from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_logger.models import Event, Remote, Action


class EventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'application', 'origin_server', 'client_ip', 'username', 'logger', 'level', 'message')
    list_filter = ('application', 'origin_server', 'username', 'logger', 'level')
    search_fields = ('application', 'origin_server', 'client_ip', 'username', 'logger', 'level', 'message')

    fieldsets = (
        (
            _('Server details'),
            {
                'fields': (
                    'timestamp',
                    'application',
                    'origin_server'
                )
            }
        ),
        (
            _('Request details'),
            {
                'fields': (
                    'client_ip',
                    'user_pk',
                    'username',
                )
            }
        ),
        (
            _('Logging details'),
            {
                'fields': (
                    'logger',
                    'level',
                    'message'
                )
            }
        ),
        (
            _('Exception details'),
            {
                'fields': (
                    'stack_trace',
                    'debug_page'
                )
            }
        )
    )


class RemoteAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'status_code')
    list_filter = ('timestamp', 'status_code')
    search_fields = ('request', 'response', 'status_code')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_username', 'action', 'object_text')
    list_filter = ('user_username', 'section', 'action')
    search_fields = ('user_username', 'section', 'action', 'object_text')


admin.site.register(Event, EventAdmin)
admin.site.register(Remote, RemoteAdmin)
admin.site.register(Action, ActionAdmin)
