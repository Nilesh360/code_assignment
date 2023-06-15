from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm,EditUserForm
from django.db.models import Q
from .user_services import getUsers,saveUser,toggle_online,cacheDataBackend
import threading
from django.core.cache import cache
import json
import string
import random

# Create your views here.

def home(request):
    toggle_online(request,'online')
    room_name = None
    connect_request_user = None 
    if request.user.is_authenticated:
        cache_obj = cacheDataBackend()
        cache_data = cache_obj.getter(request.user.id)
        if cache_data:
            room_name = cache_data['room_name']
            connect_request_userid=cache_data['connect_request_userid']
            connect_request_user = User.objects.get(id=connect_request_userid)
    context={'room_name':room_name,'connect_request_user':connect_request_user}
    return render(request,'base/home.html',context)



@login_required(login_url='login')
def logoutUser(request):
    toggle_online(request,'offline')
    logout(request)
    request.session.flush()
    return redirect('home')

def registerPage(request):
    page='register'
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user  = saveUser(request,form)
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")
    context = {'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(Q(email=username) |
                                        Q(phone=username))
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                toggle_online(request,'online')
                return redirect('home')
            else:
                messages.error(request,'Username or password does not exists')
        except:
            messages.error(request,'User does not exists')
    context={'page':page}
    return render(request,'base/login_register.html',context)

@login_required(login_url='login')
def EditUserProfile(request):
    user = User.objects.get(id=request.user.id)
    form = EditUserForm(instance=user)
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('home')
        else:
            messages.error(request,'Incorrect data in form')

    context={'form':form}
    return render(request,'base/editprofile.html',context)

@login_required(login_url='login')
def displayUser(request):
    interest = request.GET.get('interest') if request.GET.get('interest') != None else None
    users = getUsers(request,interest)
    context = {'users':users,'Interest':interest}
    return render(request,'base/Interest.html',context)

@login_required(login_url='login')
def sendUserChatRequest(request,pk):
    passed_user = User.objects.get(id=pk)
    room_name=''.join(random.choices(string.ascii_uppercase +string.digits, k=9)) # 9 length room_name
    data = {
    'connect_receiver_userid': str(pk),
    'connect_request_userid': str(request.user.id),
    'room_name':room_name
    }
    cache_obj = cacheDataBackend()
    cache_obj.setter(pk,data)
     
    context={'passed_user':passed_user,'room_name': room_name}
    return render(request,'base/chatroom.html',context)


@login_required(login_url='login')
def getRoom(request):
    cache_obj = cacheDataBackend()
    cache_data = cache_obj.getter(request.user.id)
    passed_user=None
    room_name = None
    if cache_data:
        connect_request_userid=cache_data['connect_request_userid']
        passed_user = User.objects.get(id=connect_request_userid)
        room_name = cache_data['room_name']

    cache_obj.delete(request.user.id)
    context={'passed_user':passed_user,'room_name': room_name}
    return render(request, 'base/chatroom.html', context)





