from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home.as_view(),name="home"),
    path('logout/',views.logoutUser.as_view(),name="logout"),
    path('login/',views.LoginPage.as_view(),name="login"),
    path('register/',views.registerPage.as_view(),name="register"),
    path('Display-user/',views.displayUser.as_view(),name="display-user"),
    path('connect/<str:pk>',views.sendUserChatRequest.as_view(),name="connect-user"),
    path('chat/<str:pk>',views.getRoom.as_view(),name="room"),
    path('edit-user/',views.EditUserProfile.as_view(),name="edit-user"),
]