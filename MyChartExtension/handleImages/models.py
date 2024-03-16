from django.db import models

# Create your models here.
class ChatGptBot(models.Model):
    messageInput = models.TextField()
    botResponse = models.TextField()