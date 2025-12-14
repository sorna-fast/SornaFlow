from django.shortcuts import render
from django.conf import settings
# Create your views here.

def media_admin(request):
    return {"media_url":settings.MEDIA_URL}

