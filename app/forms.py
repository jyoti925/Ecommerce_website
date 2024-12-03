from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput
                            (attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username', 'email', 'password1','password2']
        labels= {'email': 'Email'}
        widgets= {'username': forms.TextInput(attrs=
                                              {'class':'form-control'})}
    
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={'autofocus': True, 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}
        )
    )

class MyPasswordChangeForm(PasswordChangeForm):
    # You can add custom fields or validation here, if needed.
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    # Custom validation can be added here
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        
        return password2
