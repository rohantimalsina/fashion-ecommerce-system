from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm


class ContactForm(forms.ModelForm):
	class Meta:
		model=ContactUs
		fields=('name','email','subject','message')


# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')

