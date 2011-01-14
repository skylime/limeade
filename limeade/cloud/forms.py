from django import forms
from django.utils.translation import ugettext_lazy as _

class InstanceForm(forms.Form):
	name       = forms.RegexField(
		regex=r'^[a-z0-9]+$', max_length=12, widget=forms.TextInput(),
		label=_("Name"),
		error_messages={'invalid': _("This value must contain only lowercase letters and numbers.")})
	base_image = forms.ChoiceField(label = _("Image"))
	product = forms.ModelChoiceField(queryset=(), label = _("Product"))
