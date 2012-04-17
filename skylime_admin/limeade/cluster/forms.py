from django import forms
from models import Server, Region

class ServerForm(forms.ModelForm):
	class Meta:
		model = Server


class RegionForm(forms.ModelForm):
	class Meta:
		model = Region