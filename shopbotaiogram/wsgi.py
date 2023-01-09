"""
WSGI config for shopbotaiogram project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
# -*- coding: utf-8 -*-
import os
import sys

from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
# путь к проекту, там где manage.py
sys.path.insert(0, '/root/bots/shopbotaiogram')
# путь к фреймворку, там где settings.py
sys.path.insert(0, '/root/bots/shopbotaiogram/shopbotaiogram')
# путь к виртуальному окружению myenv
sys.path.insert(0, '/root/bots/shopbotaiogram/venv/lib/python3.7/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "shopbotaiogram.settings"
