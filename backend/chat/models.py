from django.db import models
from django.contrib.auth.models import User

# class Message(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
#     content = models.TextField(max_length=500)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read_status = models.BooleanField()

#     def __str__(self):
#         return self.sender.username + "->" + self.recipient.username

class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    chat_type = models.CharField(max_length=7, choices=(("default", "default"), ("support", "support")), default=("default"))

    def __str__(self) -> str:
        return self.chat_name+" "+self.chat_type


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    read_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.sender.username+"-->"+self.chat.chat_name
    