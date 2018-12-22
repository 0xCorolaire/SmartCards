# coding: utf-8

""" Vues du module de connexion """
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import User as Us


"""
API connection
"""
@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def register_api(request):
    body=json.loads(request.body)
    username = body['username']
    password = body['password']
    email = body['email']
    exist = Us.objects.get(username=username)
    if exist:
        return Response({"error":"User already exist"})
    else:
        user = Us.objects.create(username=username,password=password,email=email,elo=2000,credit=500,total_played=0,total_win=0,total_lost=0)
    return Response(True)


@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def connexion_api(request):
    """
    Endpoint de connexion
    """
    body=json.loads(request.body)
    username=body['username']
    password=body['password']
    user = authenticate(username=username,password=password)
    if user:
        return Response(True)
    else:
        return Response(False)
