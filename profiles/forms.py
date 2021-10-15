from django import forms
from .models import Profile
import bleach


class BasicForm(forms.ModelForm):
    class Meta:
        model = None
        fileds = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-main'
            field.help_text = 'not required'


class ProfileForm(BasicForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    born = forms.DateField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'born',
                  'bio', 'avatar'
                  ]
        widgets = {
            'bio': forms.Textarea(
                attrs={'cols': 20, 'rows': 20}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        unid = kwargs.pop('unid', None)
        super().__init__(*args, **kwargs)
        self.fields['born'].help_text = "not required,format example: 2020-01-30"

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        bio = bleach.clean(bio, tags=[], strip=True).strip()
        return bio


"""
no bleach vs with bleach: for input

user input: .. add some &lt;script&gt; var zoo=12 &lt;/script&gt;
vs ( without Bleach)
user input: .. add some <script> var zoo=12 </script>
"""

# def clean_born(self):
#     born = self.cleaned_data.get('born')
#     if (...) > ...:
#         raise forms.ValidationError('Not a valid date format')
#     return born
