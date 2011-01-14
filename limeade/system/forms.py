from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Product, Contract, Domain
	
class PersonForm(forms.Form):
	email = forms.EmailField(label=_("Email address"))
	first_name = forms.CharField(label = _("First name"))
	last_name = forms.CharField(label = _("Last name"))
	company = forms.CharField(label = _("Company"))
	address = forms.CharField(label = "Address")
	
class PersonAddForm(PersonForm):
	username = forms.RegexField(
		regex=r'^[a-zA-Z0-9-]+$', max_length=30, widget=forms.TextInput(),
		label=_("Username"),
		error_messages={'invalid': _("This value must contain only letters, numbers and minus.")})
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_("Password"))

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude = ['personalized', 'owner']

class ContractForm(forms.ModelForm):
	class Meta:
		model = Contract
		exclude = ['person']

class DomainForm(forms.ModelForm):
	class Meta:
		model = Domain
		exclude = ['contract']