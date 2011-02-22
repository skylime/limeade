from django.db import models
from limeade.system.models import Product, Domain
from limeade.system.utils import get_domains

default_length = 250
VHOST_STYLES = (
    ('static', 'Static'),
    ('php5',   'PHP 5.3'),
    ('wsgi',   'Python'),
)


class VHost(models.Model):
	name     = models.CharField(max_length=default_length)
	domain   = models.ForeignKey(Domain, blank=False)
	style    = models.CharField(max_length=8, choices=VHOST_STYLES)
	
	
	def __unicode__(self):
		return unicode(self.name) + '.' + unicode(self.domain)


class HTTPRedirect(models.Model):
	name   = models.CharField(max_length=default_length)
	domain = models.ForeignKey(Domain)
	to     = models.CharField(max_length=default_length)
	
	def __unicode__(self):
		return self.name + '.' + unicode(self.domain) + ' -> ' + self.to
		
class Limitset(models.Model):
	product = models.ForeignKey(Product, unique=True, related_name='limitset_web')
	vhosts    = models.IntegerField("VHosts")
	redirects = models.IntegerField("Redirects")
	webspace  = models.IntegerField("Storage", help_text="MB")
	cputime   = models.IntegerField("CPU Time")

	is_limitset = True
	@staticmethod
	def utilization(user, ressource):
		domains = get_domains(user)
		if ressource == 'accounts':
			return VHost.objects.filter(domain__in=list(domains)).count()
		if ressource == 'redirects':
			return Redirect.objects.filter(domain__in=list(domains)).count()
		return None
		
	class Meta:
		verbose_name = 'Web'


def get_vhosts(user):
	return VHost.objects.filter(domain__in=list(get_domains(user)))
