"""Models for limeade mail"""
from django.db import models
from limeade.system.models import Product, Domain
from limeade.system.utils import get_domains, md5crypt, gen_salt


# define default length for Django's ORM
default_length = 250


class Account(models.Model):
    """Creates a new mail account
    
    :param name: the name of the account
    :param domain: the foreign key to the domain
    :param password: the password of the account
    """
    name     = models.CharField(max_length=default_length)
    domain   = models.ForeignKey(Domain)
    password = models.CharField(max_length=default_length)
    
    def set_password(self, password):
        """Salt and hashes the password."""
        self.password = md5crypt(password, gen_salt())

    def __unicode__(self):
        """Unicode representation for the mail account."""
        return unicode(self.name) + '@' + unicode(self.domain)
    
    class Meta:
        unique_together = ('name', 'domain')


class Redirect(models.Model):
    """Creates a new mail redirect
    
    :param name: the name of the redirect
    :param domain: the foreign key to the domain
    :param to: redirect to
    """
    name   = models.CharField(max_length=default_length)
    domain = models.ForeignKey(Domain)
    to     = models.CharField(max_length=default_length)
    
    class Meta:
        unique_together = ('name', 'domain')
    
    def __unicode__(self):
        """Unicode representation for the mail redirect."""
        return self.name + '@' + unicode(self.domain) + ' -> ' + self.to


class Limitset(models.Model):
    """Creates a limitset.
    
    :param product: the foreign key to the product
    :param accounts: the maximum number of mail accounts
    :param redirects: the maximum number of mail redirects
    :param mailspace: the maximum number of space
    """
    product = models.ForeignKey(Product, unique=True, related_name='limitset_mail')
    accounts = models.IntegerField("Accounts")
    redirects = models.IntegerField("Redirects")
    mailspace = models.IntegerField("Storage", help_text="MB")
    
    is_limitset = True
    @staticmethod
    def utilization(user, ressource):
        """Returns the correct ressource."""
        domains = get_domains(user)
        if ressource == 'accounts':
            return Account.objects.filter(domain__in=list(domains)).count()
        if ressource == 'redirects':
            return Redirect.objects.filter(domain__in=list(domains)).count()
        return None
    
    class Meta:
        verbose_name = 'Email'

