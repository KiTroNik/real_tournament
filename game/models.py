from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Game(models.Model):
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255, blank=True, null=True)
    question_number = models.IntegerField(default=0)
    started = models.BooleanField(default=False)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(
        Game, related_name='player', on_delete=models.SET_NULL, blank=True, null=True)
    points = models.IntegerField(default=0)
    is_creator = models.BooleanField(default=False)
    in_game = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
