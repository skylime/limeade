from django import forms
from django.utils.translation import ugettext_lazy as _

# mysql username is max length 16
# we generate the mysql username with limeade_user + '_' + db_name

class DBForm(forms.Form):
	name    = forms.RegexField(
				regex=r'^[a-z0-9]+$',
				max_length=12, widget=forms.TextInput(),
				label = _("Name"),
				error_messages = {'invalid': _("This value must contain only lowercase letters and numbers.")})
		
	password = forms.CharField(min_length = 6, required = True, widget=forms.PasswordInput)
	
	
class DBEditForm(forms.Form):
	password = forms.CharField(min_length = 6, required = True, widget=forms.PasswordInput)
