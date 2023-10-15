from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class Login(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)

class UserRegister(forms.ModelForm):
  password = forms.CharField(label='Parol',widget=forms.PasswordInput)
  password_2 = forms.CharField(label='Parol 2',widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['username','first_name','email']
  def clean_password2(self):
    data = self.data
    if data['password'] != data['password2']:
      raise forms.ValidationError("Xato")

    return data['password2']


class UserEdit(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name','last_name','email']

class ProfileEdit(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['photo','data_of_birth']