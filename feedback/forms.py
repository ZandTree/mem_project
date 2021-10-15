from django import forms
from django.conf import settings
from django.core import validators

from captcha.fields import ReCaptchaField
import bleach


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label="Your name",
                           validators=[validators.MinLengthValidator(2)])

    subject = forms.CharField(max_length=120, label="Your subject")
    email = forms.EmailField(label="Your email")
    message = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 50, 'rows': 10,
               'placeholder': 'write your message'}),
        label="Message",
        max_length=3200,
        help_text="Message field can't be empty"
    )
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="",
                               validators=[validators.MaxLengthValidator(0)],
                               error_messages={"required": "should not be here"}
                               )
    if settings.USE_CAPCHA:
        captcha = ReCaptchaField(
            public_key=settings.RECAPTCHA_PUBLIC_KEY,
            private_key=settings.RECAPTCHA_PRIVATE_KEY
        )

    def clean_message(self):
        message = self.cleaned_data.get('message', 'no input')
        message = bleach.clean(message, tags=[], strip=True).strip()
        words = message.split()
        if len(words) < 3:
            raise forms.ValidationError("Your message is too short; should contain at least three words")
        return message

    def clean_name(self):
        name = self.cleaned_data.get('name', 'no input')
        name = bleach.clean(name, tags=[], strip=True).strip()
        if len(name) < 1:
            raise forms.ValidationError("Your name should contain at least one word")
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', "no input")
        subject = bleach.clean(subject, tags=[], strip=True).strip()
        if len(subject) < 1:
            raise forms.ValidationError("Subject should contain at least one word")

        return subject

    def clean_email(self):
        email = self.cleaned_data.get('email', 'no input')
        email = bleach.clean(email, tags=[], strip=True).strip()
        if not '@' in email:
            raise forms.ValidationError("Enter a valid email address")
        return email
