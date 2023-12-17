import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage
from user_service.models import CustomUser  # Adjust the import path based on your project structure

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        recipient_id = self.scope['url_route']['kwargs'].get('recipient_id')
        sender_id = self.scope['url_route']['kwargs'].get('sender_id')
        room_identifier = '_'.join(sorted([str(sender_id), str(recipient_id)]))
        self.room_group_name = f"chat_{room_identifier}"

        if room_identifier:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Send chat history to the connecting user
            chat_history = ChatMessage.get_chat_history(room_identifier)
            for message in chat_history:
                self.send(text_data=json.dumps({
                    'type': 'chat.message',
                    'message': message.message,
                    'sender': message.sender.username,  # Use the username here
                }))

            self.accept()
        else:
            print("WebSocket connection rejected: Recipient ID not provided")

    def disconnect(self, close_code):
        if self.room_group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message_text = text_data_json.get('message')
    #     sender_username = text_data_json.get('sender')

    #     if message_text and sender_username:
    #         # Fetch the sender's CustomUser instance
    #         sender_instance = CustomUser.objects.get(username=sender_username)

    #         room_identifier = self.room_group_name
    #         ChatMessage.objects.create(
    #             sender=sender_instance,
    #             message=message_text,
    #             room_id=room_identifier,
    #         )

    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_group_name,
    #             {
    #                 'type': 'chat.message',
    #                 'message': message_text,
    #                 'sender': sender_username,  # Use the username here
    #             }
    #         )
    #     else:
    #         print("Received message without 'message', 'sender_id', or 'recipient_id' key:", text_data)

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': message,
            'sender': sender,
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'get.chat_history':
            # Handle request for chat history
            chat_history = self.get_chat_history()
            self.send_chat_history(chat_history)
        else:
            # Handle regular chat messages
            self.handle_chat_message(text_data_json)


    def get_chat_history(self):
        # Fetch chat history for the current room or channel
        room_identifier = self.room_group_name
        chat_history = ChatMessage.objects.filter(room_id=room_identifier).order_by('timestamp')

        # Convert chat history to a list of dictionaries
        return [
            {
                'sender': message.sender.username,
                'message': message.message,
                'timestamp': message.timestamp.isoformat(),
            }
            for message in chat_history
        ]

    def send_chat_history(self, chat_history):
        # Send the chat history to the client
        self.send(text_data=json.dumps({
            'type': 'chat.history',
            'history': chat_history,
        }))

    def handle_chat_message(self, text_data_json):
        # Handle regular chat messages as before
        message_text = text_data_json.get('message')
        sender_username = text_data_json.get('sender')

        if message_text and sender_username :
            # Fetch the sender's CustomUser instance
            sender_instance = CustomUser.objects.get(username=sender_username)

            room_identifier = self.room_group_name
            ChatMessage.objects.create(
                sender=sender_instance,
                message=message_text,
                room_id=room_identifier,
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message_text,
                    'sender': sender_username,
                }
            )
        else:
            print("Received message without 'message', 'sender_id', or 'room_id' key:", text_data_json)