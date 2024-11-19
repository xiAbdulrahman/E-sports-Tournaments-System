from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tournament
import requests


@receiver(post_save, sender=Tournament)
def announce_tournament(sender, instance, created, **kwargs):
    if created:

        message = (f"@everyone \n"
                   f" A new {instance.game} tournament  has been created. \n"
                   f"Starting on {instance.start_date}, With a prize of {instance.prize} SAR!")
        webhook_url = ""
        data = {
            "content": message
        }
        response = requests.post(webhook_url, data=data)


