from django.db import models
from limeade.system.models import Product, Domain
from limeade.system.utils import get_domains

default_length = 250

class Account(models.Model):
	name     = models.CharField(max_length=default_length)
	domain   = models.ForeignKey(Domain)
	password = models.CharField(max_length=default_length)
	
	def __unicode__(self):
		return unicode(self.name) + '@' + unicode(self.domain)


class Redirect(models.Model):
	name   = models.CharField(max_length=default_length)
	domain = models.ForeignKey(Domain)
	to     = models.CharField(max_length=default_length)
	
	def __unicode__(self):
		return self.name + '@' + unicode(self.domain) + ' -> ' + self.to
		
class Limitset(models.Model):
	product = models.ForeignKey(Product, unique=True)
	accounts = models.IntegerField("Accounts")
	redirects = models.IntegerField("Redirects")
	mailspace = models.IntegerField("Storage", help_text="MB")

	is_limitset = True
	@staticmethod
	def utilization(user, ressource):
		domains = get_domains(user)
		if ressource == 'accounts':
			return Account.objects.filter(domain__in=list(domains)).count()
		if ressource == 'redirects':
			return Redirect.objects.filter(domain__in=list(domains)).count()
		return None
		
	class Meta:
		verbose_name = 'Email'
