"""
ASGI config for crescent project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_asgi_application()

# flake8: noqa: #402
from apps.api.routers import router as api_router

fastapp = FastAPI()
fastapp.include_router(api_router, tags=["api"], prefix="/api")
