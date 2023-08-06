# Django Logger
Log exceptions, errors and user activity for Django

## Quick start
1. Add "django_logger" to your INSTALLED_APPS setting like this::

> INSTALLED_APPS = [ ... 'django_logger', ]

2. Add 'django_logger.middleware.RequestLoggingMiddleware' to your MIDDLEWARE setting like this::
   
> MIDDLEWARE = [
    ...,
    'django_logger.middleware.RequestLoggingMiddleware',
    ]

3. Run python manage.py migrate to create the django_logger models.

4. Visit http://127.0.0.1:8000/admin/ to see logs.
