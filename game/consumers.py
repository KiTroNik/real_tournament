import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Player, Game


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        self.user = self.scope['user']

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
        # remove from game and send to socket and if creator remove game
        if self.user.player.is_creator:
            game = Game.objects.filter(room_name=self.room_name)[0]
            game.delete()

            self.user.player.game = None
            self.user.player.points = 0
            self.user.player.is_creator = False
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

    # Receive message from WebSocket
    def receive(self, text_data):
        pass

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
