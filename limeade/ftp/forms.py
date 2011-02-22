from django.forms.widgets import PasswordInput
from django import forms
from models import Account

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account


class AccountEditForm(forms.ModelForm):
	class Meta:
		model = Account
		exclude = ('name', 'vhost')
		widgets = {'password': PasswordInput(render_value=False),}
		
		
		
