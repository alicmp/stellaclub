# -*- coding: utf-8 -*-
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
	phone_number = forms.CharField(
		label='برای ورود، شماره تلفن همراه خود را وارد کنید', 
		widget=forms.TextInput(attrs={'placeholder': 'سلام', 'class':'form-control text-center'})
	)

class GetFullNameForm(forms.ModelForm):
	full_name = forms.CharField(
		label='نام و نام خانوادگی',
		widget=forms.TextInput(attrs={'placeholder': '', 'class':'form-control text-center'})
	)
	class Meta:
		model = User
		fields = [
			'full_name',
		]

class ConfirmationForm(forms.Form):
	activation_code = forms.CharField(
		label='کد تایید دریافتی روی تلفن همراه خود را در کادر زیر وارد نمایید', 
		widget=forms.TextInput(attrs={'placeholder': '', 'class':'form-control text-center'})
	)