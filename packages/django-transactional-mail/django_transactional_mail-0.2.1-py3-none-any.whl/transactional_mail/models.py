"""Models related to sending emails"""

from django.contrib.auth import get_user_model
from django.db import models

class SentMail(models.Model):
    """A log of sent emails"""
    class_name = models.CharField(max_length=64)
    email_address = models.EmailField()
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    plain_body = models.TextField()
    html_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
