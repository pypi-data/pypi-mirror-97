#!/usr/bin/env python

from django.core.management import call_command
from boot_django import boot_django

boot_django()

call_command("makemessages","-l en")
call_command("makemessages","-l pl")
