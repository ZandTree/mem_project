"""
djangoproject 3.0
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import Index

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Index.as_view(), name='index'),
    path('profile/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
    path('feedback/', include('feedback.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
