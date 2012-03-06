from django.db import models
from django.contrib.auth.models import User
from limeade.system.models import Product, Domain
from limeade.system.utils import get_domains
from OpenSSL import SSL, crypto
from x509 import parseAsn1Generalizedtime, x509name_to_str

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
	cert     = models.ForeignKey('SSLCert', blank=True, null=True, verbose_name='SSL Certificate')
	# TODO: upgrade django version to make this work:
	#cert     = models.ForeignKey('SSLCert', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='SSL Certificate')
	
	def __unicode__(self):
		return unicode(self.name) + '.' + unicode(self.domain)


class DefaultVHost(models.Model):
	domain = models.OneToOneField(Domain, blank=False)
	vhost  = models.ForeignKey(VHost, blank=False)


class SSLCert(models.Model):
	owner            = models.ForeignKey(User)
	serial           = models.CharField(max_length=default_length)
	valid_not_before = models.DateTimeField()
	valid_not_after  = models.DateTimeField()
	subject          = models.CharField(max_length=default_length)
	issuer           = models.CharField(max_length=default_length)
	cert             = models.TextField()
	key              = models.TextField()
	ca               = models.TextField()
	
	def set_cert(self, cert, key, ca):			
		self.cert = cert
		self.key  = key
		self.ca   = ca
		
		cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
			
		self.subject = x509name_to_str(cert.get_subject())
		self.issuer  = x509name_to_str(cert.get_issuer())
		self.serial  = cert.get_serial_number()
		self.valid_not_before = parseAsn1Generalizedtime(cert.get_notBefore())
		self.valid_not_after  = parseAsn1Generalizedtime(cert.get_notAfter())
			
	def __unicode__(self):
		return self.subject + ' (' + self.serial + ')'

class HTTPRedirect(models.Model):
	name   = models.CharField(max_length=default_length)
	domain = models.ForeignKey(Domain)
	to     = models.CharField(max_length=default_length)
	
	class Meta:
		unique_together = ('name', 'domain')
		
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
			return HTTPRedirect.objects.filter(domain__in=list(domains)).count()
		return None
		
	class Meta:
		verbose_name = 'Web'


def get_vhosts(user):
	return VHost.objects.filter(domain__in=list(get_domains(user)))
