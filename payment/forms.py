# -*- coding: utf-8 -*-
from django import forms
from .models import Transaction
from accounts.models import User

class TransactionForm(forms.Form):
  amount = forms.FloatField(
    widget=forms.NumberInput(attrs={'class': 'form-control text-center'}),
    label="مبلغ به تومان",
  )
  receiver = forms.CharField(
    widget = forms.HiddenInput()
  )

class CardNumForm(forms.ModelForm):
	card_num = forms.CharField(
		label='شماره کارت',
		widget=forms.TextInput(attrs={'placeholder': '', 'class':'form-control text-center'})
	)
	class Meta:
		model = User
		fields = [
			'card_num'
		]