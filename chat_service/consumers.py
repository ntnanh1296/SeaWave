import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Extract user IDs from the URL route
        recipient_id = self.scope['url_route']['kwargs'].get('recipient_id')
        current_user_id = self.scope['url_route']['kwargs'].get('sender_id')

        # Ensure a consistent room identifier based on user IDs
        room_identifier = '_'.join(sorted([str(current_user_id), str(recipient_id)]))
        self.room_group_name = f"chat_{room_identifier}"

        if room_identifier:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            print("WebSocket connection rejected: Recipient ID not provided")

    def disconnect(self, close_code):
        if self.room_identifier:
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender')

        if message:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': sender
                }
            )
        else:
            print("Received message without 'message' key:", text_data)

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
