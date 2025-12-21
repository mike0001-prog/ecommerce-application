from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import WishList

@receiver(post_save,sender=User)
def create_user_wish_list(sender,instance,created,**kwargs):
    if created:
        WishList.objects.create(user=instance)
