from django.db import models
from django.contrib.auth.models import User


class SystemMessages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messagess')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messagess')
    content = models.CharField(max_length=100)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username + "->" + self.recipient.username