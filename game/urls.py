from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, SignupView

app_name = 'game'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
