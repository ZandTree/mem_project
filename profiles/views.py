from django.shortcuts import get_object_or_404, Http404
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from .forms import ProfileForm
import mixins


class ProfileView(LoginRequiredMixin, mixins.OwnerMixin, DetailView):
    model = Profile


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "profiles/profile_update_form.html"
    form_class = ProfileForm
    succcess_message = "You've just changed your profile"

    def get_object(self, queryset=None):
        unid_ = self.kwargs.get('profile_unid')
        obj = get_object_or_404(Profile, unid=unid_, user=self.request.user)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'initial': {'user': self.request.user, 'unid': self.object.unid}})
        return kwargs

    def get_success_message(self, *args, **kwargs):
        return self.succcess_message


class DeleteProfile(LoginRequiredMixin, mixins.OwnerMixin, DeleteView):
    template_name = 'profiles/profile_delete.html'
    model = Profile
    success_url = reverse_lazy('index')
    succcess_message = "You've just deleted your profile"

    def get_success_message(self, *args, **kwargs):
        return self.succcess_message
