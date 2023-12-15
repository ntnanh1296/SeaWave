# chat_service/models.py

from django.db import models
from django.contrib.auth import get_user_model

class Chat(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name='chats')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
