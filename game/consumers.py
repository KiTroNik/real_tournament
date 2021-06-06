import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from .models import Player, Game

from quiz.models import Question
from quiz.serializers import RandomQuestionSerializer


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        self.user = self.scope['user']

        self.user.player.in_game = True
        self.user.player.save()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        message = Player.objects.filter(game__room_name=self.room_name).count()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        self.accept()

    def disconnect(self, close_code):
        if self.user.player.game.started:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
            return

        # remove from game and send to socket and if creator remove game
        if self.user.player.is_creator:
            game = Game.objects.filter(room_name=self.room_name)[0]
            game.delete()

            self.user.player.game = None
            self.user.player.points = 0
            self.user.player.is_creator = False
            self.user.player.in_game = False
            self.user.player.save()

            message = 'exit'

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            self.user.player.game = None
            self.user.player.points = 0
            self.user.player.in_game = False
            self.user.player.save()

            message = Player.objects.filter(game__room_name=self.room_name).count()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (possible: start game)
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        client_message = text_data_json['message']['event']

        if client_message == 'start' and self.user.player.is_creator:
            self.user.player.game.started = True
            self.user.player.game.save()

            message = 'start_game'
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        self.user = self.scope['user']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # remove from game and send to socket and if creator remove game
        if self.user.player.is_creator:
            game = Game.objects.filter(room_name=self.room_name)[0]
            game.delete()

            self.user.player.game = None
            self.user.player.points = 0
            self.user.player.is_creator = False
            self.user.player.in_game = False
            self.user.player.save()

            message = {
                'event': 'exit',
                'data': ''
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            self.user.player.game = None
            self.user.player.in_game = False
            self.user.player.points = 0
            self.user.player.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        client_message = text_data_json['message']['event']

        if client_message == 'next_question' and self.user.player.is_creator:
            self.send_random_questions_to_players()

    def send_random_questions_to_players(self):
        question = Question.objects.all().order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        data = json.dumps(serializer.data)
        message = {
            'event': 'change_question',
            'data': data
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
