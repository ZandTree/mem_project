from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import default_storage as storage
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from utils import create_profile_uid

from PIL import Image
import os
import io

import logging

logger = logging.getLogger(__name__)


def upload_avatar(instance, file):
    """
    make path to uploaded file (avatar) and adjust file name if needed
    unique file name thx time string
    """
    file_ext = os.path.splitext(file)[-1]  # '.jpg'
    file_name = file.split('.')[0]
    if len(file_name) > 15:
        file_name = file_name[:15]
    time = timezone.now().strftime('%Y-%m-%d')
    file_name = file_name + time
    file = file_name + file_ext
    user_folder = 'user_{}'.format(instance.id)
    return os.path.join('avatar', user_folder, file)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    unid = models.CharField(max_length=8, unique=True, blank=True)
    bio = models.TextField(blank=True, default="")
    born = models.DateField(blank=True, null=True)
    first_name = models.CharField(blank=True, default="", max_length=56)
    last_name = models.CharField(blank=True, default="", max_length=124)
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_avatar)

    def __str__(self):
        if self.first_name and self.last_name:
            first = self.first_name.capitalize()
            last = self.last_name.capitalize()
            return "{} {}".format(first, last)
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('profiles:profile', kwargs={'profile_unid': self.unid})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # let op: rb! binary
        if self.avatar:
            try:
                img_read = storage.open(self.avatar.name, 'rb')
                img = Image.open(img_read)
                # making large img 600: adjusted size
                if img.width > 200:
                    output_size = (200, 200)
                    img.thumbnail(output_size)
                in_mem_file = io.BytesIO()
                img.convert('RGB').save(in_mem_file, format='JPEG')
                img_write = storage.open(self.avatar.name, 'w+')
                img_write.write(in_mem_file.getvalue())
                img_write.close()
                img_read.close()
            except:
                msg = "Profile image user:{} failed".format(self.id)
                logger.warning(msg)


# sync creation user object and profile object
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """As New User created, create Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """As New User created, save Profile"""
    # print("save_user_profile is action")
    instance.profile.save()


# creating unique profile unid
def add_entry_slug(sender, instance, **kwargs):
    # no need to sender = some model, it happens later
    """As New Entry created, create it's slug"""
    if not instance.unid:
        instance.unid = create_profile_uid(instance)


pre_save.connect(add_entry_slug, sender=Profile)


@receiver(post_delete, sender=Profile)
def auto_delete_user(sender, instance, **kwargs):
    instance.user.delete()
