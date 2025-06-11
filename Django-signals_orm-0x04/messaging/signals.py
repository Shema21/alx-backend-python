from django.db.models.signals import post_save, pre_save,post_delete
from django.dispatch import receiver

from .models import Message, MessageHistory, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = Message.objects.get(pk=instance.id)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=old_instance,
                    content=old_instance.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass  # message is new

@receiver(post_delete, sender=User)
def clean_user_content(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()