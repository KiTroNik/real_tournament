from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz_api/', include('quiz.urls', namespace='quiz_api')),
    path('', include('game.urls', namespace='game')),
]
