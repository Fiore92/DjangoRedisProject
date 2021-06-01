from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginAuth, name='login'),
    path('signin/',views.signIn,name='signIn'),
    path('LogOut/',views.LogOut,name='LogOut'),
    path('home/',views.home,name='home'),
    path('reservedArea/',views.reservedArea,name='reservedArea'),
    path('userArea/<int:pk>/',views.userArea),
    path('endpoint/',views.endPoint1),
    path('endpoint2/',views.endPoint2),
]