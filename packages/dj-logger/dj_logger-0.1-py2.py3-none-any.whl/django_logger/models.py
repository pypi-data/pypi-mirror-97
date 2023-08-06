import socket
from datetime import datetime, timedelta, tzinfo

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    import pytz
except ImportError:
    pytz = None

ZERO = timedelta(0)


class UTC(tzinfo):
    """
    UTC implementation taken from Python's docs.

    Used only when pytz isn't available.
    """

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


def now():
    if getattr(settings, 'USE_TZ', False):
        if pytz:
            utc = pytz.utc
        else:
            utc = UTC()
        return datetime.utcnow().replace(tzinfo=utc)
    else:
        return datetime.now()


class Event(models.Model):
    timestamp = models.DateTimeField(db_index=True, default=now)

    application = models.CharField(
        max_length=256,
        help_text=_("The application logging this record."),
        db_index=True
    )

    origin_server = models.CharField(
        max_length=256,
        help_text=_("The server logging this record."),
        default=socket.gethostname,
        db_index=True
    )

    client_ip = models.CharField(
        max_length=128,
        help_text=_("The IP address of the client making the request."),
        blank=True,
        db_index=True
    )

    user_id = models.IntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text=_("The primary key of the user making the request in which this record was logged."),
    )

    username = models.CharField(
        max_length=256,
        help_text=_("The username of the user making the request in which this record was logged."),
        blank=True,
        db_index=True
    )

    uuid = models.CharField(
        max_length=256,
        help_text=_("The UUID of the Django request in which this record was logged."),
        blank=True,
        db_index=True
    )

    logger = models.CharField(
        max_length=1024,
        help_text=_("The name of the logger of the record."),
        db_index=True
    )

    level = models.CharField(
        max_length=32,
        help_text=_("The level of the log record (DEBUG, INFO...)"),
        db_index=True
    )

    message = models.TextField()
    stack_trace = models.TextField(blank=True)
    debug_page = models.TextField(blank=True)

    class Meta:
        app_label = 'django_logger'
        ordering = ('-timestamp',)
        permissions = (
            ("view_logs", "Can view log records"),
        )


class Remote(models.Model):
    request = models.TextField()
    response = models.TextField(null=True)
    status_code = models.IntegerField(default=200)
    timestamp = models.DateTimeField(db_index=True, default=now)
    uuid = models.CharField(
        max_length=256,
        help_text=_("The UUID of the Django request in which this record was logged."),
        blank=True,
        db_index=True
    )
    user_agent = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'django_logger'
        ordering = ('-timestamp',)
        permissions = (
            ("views_logs", "Can view log records"),
        )


class Action(models.Model):

    SECTION_CONSOLE = 'console'
    SECTION_LOGIN = 'login_screen'
    SECTION_ADMIN = 'admin_screen'

    SECTION_CHOICES = (
        (SECTION_CONSOLE, _('Console')),
        (SECTION_LOGIN, _('Console')),
        (SECTION_ADMIN, _('Admin')),
    )

    ACTION_LOG_IN = 'log_in'
    ACTION_LOG_OUT = 'log_out'
    ACTION_CHANGE_PASSWORD = 'change_password'
    ACTION_USER_UPDATE = 'user_update'
    ACTION_USER_DELETE = 'user_moderate'

    ACTION_CHOICES = (
        (ACTION_LOG_IN, _('Log In')),
        (ACTION_LOG_OUT, _('Log Out')),
        (ACTION_CHANGE_PASSWORD, _('Change Password')),
        (ACTION_USER_UPDATE, _('User Update')),
        (ACTION_USER_DELETE, _('User Delete')),
    )

    timestamp = models.DateTimeField(
        db_index=True,
        default=now
    )

    user_id = models.IntegerField(
        db_index=True,
        help_text=_("The primary key of the user making the request in which this record was logged."),
    )

    user_username = models.CharField(
        db_index=True,
        max_length=255,
        help_text=_("The username of the user making the request in which this record was logged."),
    )

    user_detail = models.TextField(
        null=True
    )

    section = models.CharField(
        db_index=True,
        max_length=255,
        choices=SECTION_CHOICES,
        help_text=_("The Backend/APP section in which this record was logged.")
    )

    action = models.CharField(
        db_index=True,
        max_length=255,
        choices=ACTION_CHOICES,
        help_text=_("The Backend/APP action in which this record was logged."),
    )

    object_id = models.IntegerField(
        db_index=True,
        null=True,
        help_text=_("The primary key of the object in which this record was logged."),
    )

    object_text = models.CharField(
        db_index=True,
        max_length=255,
        null=True,
        help_text=_("The name or definition of the object in which this record was logged."),
    )

    object_detail = models.TextField(
        null=True
    )

    value_previous = models.TextField(
        null=True,
        help_text=_("The previous value when this record was logged."),
    )

    value_current = models.TextField(
        null=True,
        help_text=_("The current value when this record was logged."),
    )

    class Meta:
        app_label = 'django_logger'
        ordering = ('-timestamp',)
        permissions = (
            ("view_logs", "Can view log records"),
        )

    def __str__(self):
        return "%s" % self.action

    def __unicode__(self):
        return u"%s" % self.action
