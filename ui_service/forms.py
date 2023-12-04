from django import forms
from user_service.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from post_service.models import Post


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['text', 'media']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'gender', 'birthday']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


