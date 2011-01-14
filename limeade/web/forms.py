from django import forms
from models import VHost, HTTPRedirect as Redirect

class VHostForm(forms.ModelForm):
	class Meta:
		model = VHost

class VHostEditForm(forms.ModelForm):
	class Meta:
		model = VHost
		exclude = ('name', 'domain')

class RedirectForm(forms.ModelForm):
	class Meta:
		model = Redirect
		
