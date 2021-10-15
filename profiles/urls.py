from django.urls import path
from .views import ProfileView,UpdateProfile,DeleteProfile
app_name = "profiles"

urlpatterns = [
            path('<profile_unid>/',ProfileView.as_view(),name="profile"),
            path('update/<profile_unid>/',UpdateProfile.as_view(),name="profile-update"),
            path('delete-profile/<profile_unid>/',DeleteProfile.as_view(),name='profile-delete'),

            ]