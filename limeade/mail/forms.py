from django import forms
from models import Account, Redirect

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account


class AccountEditForm(forms.ModelForm):
	class Meta:
		model = Account
		exclude = ('name', 'domain')
		

class RedirectForm(forms.ModelForm):
	class Meta:
		model = Redirect
		
