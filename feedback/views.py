from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import get_template

from .forms import ContactForm

import logging

logger = logging.getLogger(__name__)



class Contact(View):
    template_name = 'feedback/feedback.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            host = request.get_host()
            port = request.get_port()
            logger.warning("{} {}with {} host {} port {}".format(
                request.user, name, email, host, port)
            )
            context = {
                'user': name,
                'subject': subject,
                'email': email,
                'message': message
            }
            from_email = email
            to_email = ('tspan2017@gmail.com',)
            contact_message = get_template('feedback/contact_message.txt').render(context)
            send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        else:
            print("form not valid")
            return render(request, self.template_name, {'form': form})
        return redirect("/")
