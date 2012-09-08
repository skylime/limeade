""" Models for limeade web"""
from django.db import models
from django.contrib.auth.models import User
from limeade.system.models import Product, Domain
from limeade.system.utils import get_domains
from OpenSSL import SSL, crypto
from x509 import parseAsn1Generalizedtime, x509name_to_str
from limeade.cluster.models import Region

default_length = 250
VHOST_STYLES = (
    ('static', 'Static'),
    ('php',    'PHP 5.3'),
    ('wsgi',   'Python'),
)


class VHost(models.Model):
    """Creates a vhost.
    
    :param name: the name of the Vhost
    :param domain: foreign key to the domain
    :param style: php or python vhost
    :param cert: the ssl cert
    
    :Example:
    
        >>> from limeade.web.models import VHost
        >>> vhost = VHost.objects.get(pk=1)
        >>> vhost
        <Person: Test VHost.testdomain.de>
    
    """
    name     = models.CharField(max_length=default_length)
    domain   = models.ForeignKey(Domain, blank=False)
    style    = models.CharField(max_length=8, choices=VHOST_STYLES)
    cert     = models.ForeignKey('SSLCert', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='SSL Certificate')
    
    unique_together = (("name", "domain"),)
    
    def __unicode__(self):
        """Unicode representation for the vhost."""
        return unicode(self.name) + '.' + unicode(self.domain)


class DefaultVHost(models.Model):
    """Saves the default VHost.
    
    :param doamin: the foreign key to the domain
    :param vhost: the foreign key to the vhost
    """
    domain = models.OneToOneField(Domain, primary_key=True)
    vhost  = models.ForeignKey(VHost, blank=False)


class PoolIP(models.Model):
    """The IP address pool.
    
    :param ip: the IP
    :param region: the foreign key to the region
    
    :Example:
    
        >>> from limeade.web.models import PoolIP
        >>> ip = PoolIP.objects.get(pk=1)
        >>> ip
        <Person: 127.0.0.1>
    
    """
    ip     = models.IPAddressField(unique=True, blank=False)
    region = models.ForeignKey(Region, blank=False)
    
    def __unicode__(self):
        """Unicode representation for the ip."""
        return unicode(self.ip)

class SSLCert(models.Model):
    """Creates SSL Certifications
    
    :param owner: the user
    :param serial: the ssl cert
    :param valid_not_before: date of valid
    :param valid_not_after: date of valid
    :param subject: topic of cert
    :param cn: cert number
    :param issuer: the person
    :param cert: the cert
    :param key: key of the cert
    :param ca: the ca of the cert
    :param ip: the foreign key to the ip
    """
    owner            = models.ForeignKey(User)
    serial           = models.CharField(max_length=default_length)
    valid_not_before = models.DateTimeField()
    valid_not_after  = models.DateTimeField()
    subject          = models.CharField(max_length=default_length)
    cn               = models.CharField(max_length=default_length)
    issuer           = models.CharField(max_length=default_length)
    cert             = models.TextField()
    key              = models.TextField()
    ca               = models.TextField()
    ip               = models.ForeignKey(PoolIP, unique=True, blank=False)
    
    def set_cert(self, cert, key, ca):
        """Saves the certification."""
        self.cert = cert
        self.key  = key
        self.ca   = ca
        
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            
        self.subject = x509name_to_str(cert.get_subject())
        self.issuer  = x509name_to_str(cert.get_issuer())
        self.cn      = cert.get_subject().commonName
        self.serial  = cert.get_serial_number()
        self.valid_not_before = parseAsn1Generalizedtime(cert.get_notBefore())
        self.valid_not_after  = parseAsn1Generalizedtime(cert.get_notAfter())
            
    def __unicode__(self):
        """Unicode representation for the cert."""
        return self.cn + ' (' + self.serial + ')'

class HTTPRedirect(models.Model):
    """Creates http redirects
    
    :param name: the name of the redirect
    :param doamin: the associated domain
    :param to: the redirect to
    """
    name   = models.CharField(max_length=default_length)
    domain = models.ForeignKey(Domain)
    to     = models.CharField(max_length=default_length)
    
    class Meta:
        unique_together = ('name', 'domain')
        
    def __unicode__(self):
        """Unicode representation for the redirect."""
        return self.name + '.' + unicode(self.domain) + ' -> ' + self.to
        
class Limitset(models.Model):
    """Maximum limit available.
    
    :param products: the foreign key to the product
    :param vhosts: maximum vhosts
    :param redirects: maximum redirects
    :param webspace: maximum webspace
    :param cputime: maximum cputime
    """
    product = models.ForeignKey(Product, unique=True, related_name='limitset_web')
    vhosts    = models.IntegerField("VHosts")
    redirects = models.IntegerField("Redirects")
    webspace  = models.IntegerField("Storage", help_text="MB")
    cputime   = models.IntegerField("CPU Time")

    is_limitset = True
    @staticmethod
    def utilization(user, ressource):
        """Filters specific ressources."""
        domains = get_domains(user)
        if ressource == 'accounts':
            return VHost.objects.filter(domain__in=list(domains)).count()
        if ressource == 'redirects':
            return HTTPRedirect.objects.filter(domain__in=list(domains)).count()
        return None
        
    class Meta:
        verbose_name = 'Web'


def get_vhosts(user):
    """Returns all vhosts that belongs to one user."""
    return VHost.objects.filter(domain__in=list(get_domains(user)))

