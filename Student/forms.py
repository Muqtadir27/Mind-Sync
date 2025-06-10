from django import forms
from django import forms
from .models import User

from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class SignUpForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={
            'class': 'u-input u-input-rectangle',
            'placeholder': 'Enter The Phone Number'
        })
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'studentid', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter your Name'}),
            'email': forms.EmailInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter a valid email address'}),
            'studentid': forms.TextInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter Your ID'}),
            'password': forms.PasswordInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter your Password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Password hashing
        user.phone_number = self.cleaned_data.get('phone')
        if commit:
            user.save()
        return user


from django import forms

class LoginForm(forms.Form):
    studentid = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter your Student ID'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'u-input u-input-rectangle', 'placeholder': 'Enter your Password'})
    )

