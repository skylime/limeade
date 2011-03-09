from django import forms
from django.utils.translation import ugettext_lazy as _
from models import SSHKey

class InstanceForm(forms.Form):
	hostname = forms.RegexField(regex = r'^[a-z0-9-.]+$', max_length = 64,
		error_messages={'invalid': _("This must be a valid hostname.")}
	)
	base_image = forms.ChoiceField(label = _("Image"))
	product = forms.ModelChoiceField(queryset=(), label = _("Product"))
	sshkeys = forms.ModelMultipleChoiceField(queryset=(), label = _("SSH Keys"), required = False)


class SSHKeyForm(forms.ModelForm):
	class Meta:
		model = SSHKey
		exclude = ('owner')