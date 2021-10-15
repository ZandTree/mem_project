from django.shortcuts import get_object_or_404
from django.http import Http404


class OwnerMixin:
    """ expects standard url <[model name]_unid> to work with"""
    model = None

    def get_object(self, queryset=None):
        model_name = self.model.__name__.lower()
        url_unid = "{}_unid".format(model_name)
        unid_ = self.kwargs.get(url_unid)
        obj = get_object_or_404(self.model, unid=unid_, user=self.request.user)
        if obj.user != self.request.user:
            raise Http404
        return obj


class HeaderWizard:
    header_title = ""

    def get_header_title(self):
        return self.header_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_title'] = self.get_header_title
        return context
