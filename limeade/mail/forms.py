from django import forms
from django.forms.widgets import PasswordInput
from models import Account, Redirect

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		widgets = {'password': PasswordInput(render_value=False),}


class AccountEditForm(forms.ModelForm):
	class Meta:
		model = Account
		exclude = ('name', 'domain')
		widgets = {'password': PasswordInput(render_value=False),}
		

class RedirectForm(forms.ModelForm):
	class Meta:
		model = Redirect
		
