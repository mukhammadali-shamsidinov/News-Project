from django import forms
from .models import Contact, Comments


class ContactForms(forms.ModelForm):

  class Meta:
    model = Contact
    fields = "__all__"




class CommentForm(forms.ModelForm):
  class Meta:
    model = Comments
    fields = ['body']