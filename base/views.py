from django.shortcuts import render,redirect
from .models import User,ConnectionRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm,EditUserForm
from django.db.models import Q
from .user_services import getUsers,saveUser,toggle_online
import threading
from django.core.cache import cache
import json
import string
import random
from rest_framework.decorators import APIView
from django.utils.decorators import method_decorator

# Create your views here.
class home(APIView):
    def get(self,request):
        toggle_online(request,'online')
        room_name = None
        connect_request_user = None 
        if request.user.is_authenticated:
            connect_request_user = ConnectionRequest.objects.filter(sent_to=request.user)
            print(connect_request_user)
        context={'room_name':room_name,'connect_request_user':connect_request_user}
        return render(request,'base/home.html',context)



@method_decorator(login_required(login_url='login'), name='dispatch')
class logoutUser(APIView):
    def get(self,request):
        toggle_online(request,'offline')
        logout(request)
        request.session.flush()
        return redirect('home')


class registerPage(APIView):
    def get(self,request):
        page='register'
        form = UserCreationForm()
        context = {'page':page,'form':form}
        return render(request,'base/login_register.html',context)
    def post(self,request):
            form = UserCreationForm(request.POST)
            print("form checker = ",form.is_valid())
            if form.is_valid():
                user  = saveUser(request,form)
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"An error occurred during registration")
                return redirect('register')
class LoginPage(APIView):
    def get(self,request):
        page='login'
        if request.user.is_authenticated:
            return redirect('home')
        context={'page':page}
        return render(request,'base/login_register.html',context)
    
    def post(self,request):
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
                return redirect('login')
        except:
            messages.error(request,'User does not exists')
            return redirect('login')



@method_decorator(login_required(login_url='login'), name='dispatch')
class EditUserProfile(APIView):
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        form = EditUserForm(instance=user)
        context={'form':form}
        return render(request,'base/editprofile.html',context)
    
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        form = EditUserForm(instance=user)
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('home')
        else:
            messages.error(request,'Incorrect data in form')
            return redirect('edit-user')


@method_decorator(login_required(login_url='login'), name='dispatch')
class displayUser(APIView):
    def get(self,request):
        interest = request.GET.get('interest') if request.GET.get('interest') != None else None
        users = getUsers(request,interest)
        context = {'users':users,'Interest':interest}
        return render(request,'base/Interest.html',context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class sendUserChatRequest(APIView):
    def get(self,request,pk):
        passed_user = User.objects.get(id=pk)
        room_name=''.join(random.choices(string.ascii_uppercase +string.digits, k=9)) # 9 length room_name
        data  = ConnectionRequest.objects.create(
            sent_by = request.user,
            room_name = room_name,
            sent_to = passed_user
        )
        context={'passed_user':passed_user,'room_name': room_name}
        return render(request,'base/chatroom.html',context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class getRoom(APIView):
    def get(self,request,pk):
        connection = ConnectionRequest.objects.get(id=pk)
        sent_by=None
        room_name = None
        if connection:
            sent_by=connection.sent_by
            sent_to = connection.sent_to
            room_name = connection.room_name
            connection.delete()
        context={'passed_user':sent_to,'room_name': room_name}
        return render(request, 'base/chatroom.html', context)





