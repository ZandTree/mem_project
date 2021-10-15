from django.contrib import admin
from django.db import models

from tinymce.widgets import TinyMCE
from .models import Post


class PostFormAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'img', 'tags']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()}}


admin.site.register(Post, PostFormAdmin)
