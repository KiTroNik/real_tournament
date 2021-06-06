from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import reverse, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Game, Player


class SignupView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('game:login')


class HomeView(TemplateView):
    template_name = 'home.html'


class CreateRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'game/create_room.html'


class JoinRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'game/join_room.html'


# Create game and set current user as creator
@login_required
def create_room(request, room_name):
    game = Game(creator=request.user, room_name=room_name)
    game.save()

    request.user.player.game = game
    request.user.player.is_creator = True
    request.user.player.save()

    return redirect(f'/{room_name}/')


@login_required
def join_room(request, room_name):
    game = Game.objects.filter(room_name=room_name)
    if game:
        request.user.player.game = game[0]
        request.user.player.save()

        return render(request, 'game/lobby.html', {'room_name': room_name})
    else:
        return redirect('/')


@login_required
def start_game(request, room_name):
    game = Game.objects.filter(room_name=room_name)
    if game and game[0].started:
        return render(request, 'game/game.html', {'room_name': room_name})
    else:
        return redirect('/')
