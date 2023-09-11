from .models import User
from django.core.exceptions import *
from django.contrib import messages
import json
from django.core.cache import cache


def getUsers(request,interest):
    users=None
    if interest is not None:
        users = User.objects.filter(interests__name__icontains=interest, online=True).exclude(id = request.user.id).order_by('-online')

    if interest is None or users.exists() == False:
        users = User.objects.filter(online=True).exclude(id=request.user.id)

    return users

def saveUser(request,form):
    user = form.save(commit=False)
    user.username = user.username.lower()
    user.make_password(request.POST.get('password'))
    user.online = True
    user.save()
    messages.error(request,"Registration successfull !")
    return user

def toggle_online(request,type):
    if request.user.is_authenticated:
        user = request.user
        if type == 'online':
            user.online = True
        else:
            user.online = False
        user.save()




    
        



        


