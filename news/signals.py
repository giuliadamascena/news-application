from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from .models import User  # Make sure this matches your actual import path

from django.dispatch import Signal

# Define custom signal
article_approved_signal = Signal()


@receiver(article_approved_signal)
def notify_article_approved(sender, instance, **kwargs):
    print(f"[Signal] Article '{instance.title}' by {instance.author} was approved.")
@receiver(post_save, sender=User)


def assign_user_group(sender, instance, created, **kwargs):
    """
    Assign a user to a group based on their flags.
    Example: is_journalist, is_editor
    """
    if created:
        # Remove user from all groups first (optional safety step)
        instance.groups.clear()

        if instance.is_superuser:
            return  # Skip group assignment for superusers

        # Assign group based on user flags
        if hasattr(instance, 'is_editor') and instance.is_editor:
            group, _ = Group.objects.get_or_create(name='Editor')
            instance.groups.add(group)

        elif hasattr(instance, 'is_journalist') and instance.is_journalist:
            group, _ = Group.objects.get_or_create(name='Journalist')
            instance.groups.add(group)

        else:
            # Default to Reader
            group, _ = Group.objects.get_or_create(name='Reader')
            instance.groups.add(group)


