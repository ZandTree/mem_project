from django.urls import path
from .views import Contact

app_name = "feedback"

urlpatterns = [
    path('', Contact.as_view(), name='feedback'),
]
