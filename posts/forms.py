from django import forms
from .models import Post
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class BasicForm(forms.ModelForm):
    class Meta:
        model = None
        fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "input-main"
            field.help_text = "this field not required"


class PostForm(BasicForm):
    content = forms.CharField(widget=TinyMCE(mce_attrs={'width': 800}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'img', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = "this field is required"

    def clean_content(self):
        """
        check if input contains tags (< or script) and raise error if it does
        """
        content = self.cleaned_data.get('content', None)
        if '&lt;script' in content:
            raise forms.ValidationError("These tags are not allowed")
        return content


class DateForm(forms.Form):
    """ based on datetimepicker fengyuanchen widget"""
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'archive-inp',
            'data-target': '#datepicker'
        })
    )
