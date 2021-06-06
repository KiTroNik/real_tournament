from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, SignupView, CreateRoomView, JoinRoomView
from . import views

app_name = 'game'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_room/', CreateRoomView.as_view(), name='create_room'),
    path('join_room/', JoinRoomView.as_view(), name='join_room'),
    path('create/<str:room_name>/', views.create_room, name='create'),
    path('game/<str:room_name>/', views.start_game, name='start'),
    path('<str:room_name>/', views.join_room, name='join'),
]
