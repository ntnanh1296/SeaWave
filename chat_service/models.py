# In models.py (assuming you have a models.py file in your app)
from django.db import models
from user_service.models import CustomUser  # Adjust the import based on your actual User model

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    # recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_id = models.CharField(max_length=255)  # Assuming room ID is a string, adjust as needed

    @classmethod
    def get_chat_history(cls, room_id):
        return cls.objects.filter(room_id=room_id).order_by('id')
    
    def __str__(self):
        return f"{self.sender} to {self.room_id}: {self.message}"
