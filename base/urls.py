from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('logout/',views.logoutUser,name="logout"),
    path('login/',views.LoginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('Display-user/',views.displayUser,name="display-user"),
    path('connect/<str:pk>',views.sendUserChatRequest,name="connect-user"),
    path('chat/',views.getRoom,name="room"),
    path('edit-user/',views.EditUserProfile,name="edit-user"),
]