from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ArgProfile
# form for changes to profile
class changes(forms.ModelForm):
    # defines email field
    email = forms.EmailField()
    # defines the field and model
    class Meta:
        model = User
        fields = ['email']



# additional changes to profile
class changespro(forms.ModelForm):
    class Meta:
        # changes the picture
        model = ArgProfile
        fields = ['pict']

# changes the field
class changesfield(forms.ModelForm):
    class Meta:
        model = ArgProfile
        # changes the specalist
        fields = ['specalist']

class ArgRegister(UserCreationForm):
    # adds email to user register form
    email = forms.EmailField()

# creates user register form
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
