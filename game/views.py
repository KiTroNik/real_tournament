from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('game:login')


class HomeView(TemplateView):
    template_name = 'home.html'
