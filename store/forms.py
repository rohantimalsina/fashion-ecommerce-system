from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['place', 'city', 'state']
        widgets = {'place':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nearest Places'}), 'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), 'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State or Province'})}