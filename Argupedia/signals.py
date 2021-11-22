from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ArgProfile

# reciever method used
@receiver(post_save, sender=User)
# defines the methods to create the profile
def profilecreate(sender, instance, created,*args,  **kwargs):
    # if created, creates the profile for the user logged in
    if created:
        ArgProfile.objects.create(user=instance)

# reciever method to save profile changes
@receiver(post_save, sender=User)
# saves profile changes
def profilesave(sender, instance, *args, **kwargs):
    # saves profile
    instance.argprofile.save()