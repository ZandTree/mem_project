from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.files.storage import default_storage as storage
from django.shortcuts import reverse

import io
import os

from PIL import Image

from utils import generate_unique_unid_slug
from taggit.managers import TaggableManager

import logging

logger = logging.getLogger(__name__)


def upload_post_img(instance, filename):
    """
    make media path to store post image
    add time to make file name unique inside the folder
    """
    time = timezone.now().strftime('%Y-%m-%d')
    file_ext = os.path.splitext(filename)[-1]
    start_file = filename.split(".")[0]
    if len(start_file) < 5:
        generic_file_name = start_file + time
    else:
        generic_file_name = start_file[:5] + time
    filename = generic_file_name + file_ext
    post_folder = 'post_{}'.format(instance.id)
    return os.path.join('image', post_folder, filename)


class Post(models.Model):
    # should be user ipv author to use mixin
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=124,
                             help_text='this field is required')
    content = models.TextField(blank=True, default="")
    unid = models.SlugField(blank=True, max_length=124, )
    draft = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    changed = models.DateField(auto_now=True)
    img = models.ImageField(blank=True, null=True, upload_to="upload_post_img")
    tags = TaggableManager(blank=True, help_text="List of tags separated by comma")

    def get_absolute_url(self):
        """ post_unid for mixin and url """
        return reverse('posts:post', kwargs={'post_unid': self.unid})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img:
            try:
                img_read = storage.open(self.img.name, 'rb')
                img = Image.open(img_read)
                # making large img 600: adjusted size
                if img.width > 600:
                    output_size = (600, 600)
                    img.thumbnail(output_size)
                in_mem_file = io.BytesIO()
                img.convert('RGB').save(in_mem_file, format='JPEG')
                img_write = storage.open(self.img.name, 'w+')
                img_write.write(in_mem_file.getvalue())
                img_write.close()
                img_read.close()
            except:
                logger.warning("Post image try failed")


@receiver(pre_save, sender=Post)
def add_entry_unid_slug(sender, instance, *args, **kwargs):
    """As New Post created, create it's unid(slug)"""
    if not instance.unid:
        instance.unid = generate_unique_unid_slug(instance)
