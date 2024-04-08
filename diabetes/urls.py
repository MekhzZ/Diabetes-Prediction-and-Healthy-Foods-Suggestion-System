from django.urls import path,include
from . import views

urlpatterns = [
  path('login/', views.signin, name ='login'),
  path('register/', views.register, name ='register'),
  path('profile/',views.profile , name='profile'),
  path('profile/input1',views.input1 , name='input1'),
  path('profile/calorie_calc',views.calorie_calc, name='calorie_calc'),
  path('profile/logout/', views.signout, name ='logout'),
  path('profile/history/', views.history, name ='history')
]