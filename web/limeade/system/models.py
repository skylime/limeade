from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


# define default length for Django's ORM
default_length = 250


class Person(models.Model):
    """Creates a user profile for any registered person.
    
    :param user: the user stored in django.auth.models.User
    :param company: if available, the company the user belongs to
    :param address: default address of user
    :param parent: persons can have own customers (e.g. reseller > customer)
    
    :Example:
    
        >>> from limeade.system.models import Person
        >>> person = Person.objects.get(pk=1)
        >>> person
        <Person: Test User (Test Company)>
    """
    user      = models.OneToOneField(User, primary_key=True, verbose_name=_('User'))
    company   = models.CharField(max_length=default_length, blank=True, verbose_name=_('Company'))
    address   = models.CharField(max_length=default_length, verbose_name=_('Address'))
    parent    = models.ForeignKey('self', null=True, blank=True, verbose_name=_('Parent User'))
    
    def first_name(self):
        """Returns the first name of the user."""
        return self.user.first_name
    
    def last_name(self):
        """Returns the last name of the user."""
        return self.user.last_name
    
    def username(self):
        """Returns the username of the user."""
        return self.user.username
    
    def system_user_name(self):
        """Returns unicode representation of the username."""
        return settings.SYSTEM_USER_NAME % self.username()
    
    def system_user_home(self):
        """Returns home directory of the user."""
        return settings.SYSTEM_USER_HOME % self.username()
    
    def system_user_id(self):
        """Returns the user id."""
        return settings.SYSTEM_USER_ID_OFFSET + self.pk
    
    def __unicode__(self):
        """Unicode representation for the user."""
        return self.user.first_name + ' ' + self.user.last_name + (' (' + self.company + ')' if self.company else '')
    
    class Meta:
        """Meta information of any person"""
        permissions = (
            ('customer', 'Can manage account'),
            ('reseller', 'Can manage customers'),
            ('admin',    'Can manage resellers'),
        )
        ordering = ['user',]
        verbose_name = _(u'Person')
        verbose_name_plural = _(u'Persons')


class Product(models.Model):
    """Defines a product which belongs to a person.
    
    :param name: name of the product
    :param personalized: true if its, othwerwise false
    :param owner: the person who owns this product
    
    :Example:
    
        >>> from limeade.system.models import Product
        >>> product = Product.objects.get(pk=1)
        >>> product
        <Product: Testproduct>
    """
    name         = models.CharField(max_length=default_length, verbose_name=_('Name'))
    personalized = models.BooleanField(verbose_name=_('Personalized?'))
    owner        = models.ForeignKey(User, verbose_name=_('Owner'))
    
    def __unicode__(self):
        """Unicode representation for the product."""
        return self.name
    
    def queryset(self, request):
        """Returns a filtered queryset."""
        return Product.objects.filter(owner=request.user)
    
    def has_add_permission(self, request):
        """Returns true if user has permission to add."""
        return True
    
    def has_change_permission(self, request, obj):
        """Returns true if user has permission to change."""
        return (obj.owner == request.user)
    
    def has_delete_permission(self, request, obj):
        """Returns true if user has permission to delete."""
        return (obj.owner == request.user)


class Contract(models.Model):
    """Creates a contract for a person with a product.
    
    :param person: the person
    :param product: the product
    
    :Example:
    
        >>> from limeade.system.models import Contract
        >>> contract = Contract.objects.get(pk=1)
        >>> contract
        <Contract: Testuser / Testproduct>
    """
    person  = models.ForeignKey(User, verbose_name=_('Person'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    
    def __unicode__(self):
        """Unicode representation of the contract"""
        return unicode(self.person) + ' / ' + unicode(self.product)
    
    def queryset(self, request):
        """Returns a filtered queryset by request."""
        return Contract.objects.filter(person__user__parent=request.user)
    
    def has_add_permission(self, request):
        """Returns true if user has permission to add a contract."""
        return True
    
    def has_change_permission(self, request, obj):
        """Returns true if user has permission to change the contract."""
        return (obj.owner == request.user)
    
    def has_delete_permission(self, request, obj):
        """Returns true if user has permission to delete the contract."""
        return (obj.owner == request.user)


class Domain(models.Model):
    """Model for a domain, which belongs to a contract.
    
    :param contract: the contract
    :param name: the name of the domain
    
    :Example:
    
        >>> from limeade.system.models import Domain
        >>> domain = Domain.objects.get(pk=1)
        >>> domain
        <Domain: testdomain.com>
    
    .. note:: name of domain must be unique
    """
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'))
    name = models.CharField(max_length=default_length, unique=True, verbose_name=_('Name'))
    
    def owner(self):
        """Returns the owner of the domain."""
        return self.contract.person
    
    def __unicode__(self):
        """Unicode representation of the domain."""
        return self.name


def create_user_profile(sender, instance, created, **kwargs):
    """This function creates a user profile for Django's get_profile() method, 
    after the user is registered. This works with signals."""
    if created:
        Person.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

