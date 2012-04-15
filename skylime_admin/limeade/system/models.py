from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings

default_length = 250

class Person(models.Model):
	user      = models.OneToOneField(User, primary_key=True)
	company   = models.CharField(max_length=default_length, blank=True)
	address   = models.CharField(max_length=default_length)
	parent    = models.ForeignKey('self', null=True, blank=True)

	def first_name(self):
		return self.user.first_name
	
	def last_name(self):
		return self.user.last_name
		
	def username(self):
		return self.user.username
	
	def system_user_name(self):
		return settings.SYSTEM_USER_NAME % self.username()
	
	def system_user_home(self):
		return settings.SYSTEM_USER_HOME % self.username()
	
	def system_user_id(self):
		return settings.SYSTEM_USER_ID_OFFSET + self.pk
			
	def __unicode__(self):
		return self.user.first_name + ' ' + self.user.last_name + (' (' + self.company + ')' if self.company else '')

	class Meta:
		permissions = (
			('customer', 'Can manage account'),
			('reseller', 'Can manage customers'),
			('admin',    'Can manage resellers')
		)

class Product(models.Model):
	name = models.CharField(max_length=default_length)
	personalized = models.BooleanField()
	owner = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

	def queryset(self, request):
		return Product.objects.filter(owner=request.user)
	
	def has_add_permission(self, request):
		return True
	
	def has_change_permission(self, request, obj):
		return (obj.owner == request.user)
	
	def has_delete_permission(self, request, obj):
		return (obj.owner == request.user)
			
class Contract(models.Model):
	person  = models.ForeignKey(User)
	product = models.ForeignKey(Product)

	def __unicode__(self):
		return unicode(self.person) + ' / ' + unicode(self.product)

	def queryset(self, request):
		return Contract.objects.filter(person__user__parent=request.user)
	
	def has_add_permission(self, request):
		return True
	
	def has_change_permission(self, request, obj):
		return (obj.owner == request.user)
	
	def has_delete_permission(self, request, obj):
		return (obj.owner == request.user)


class Domain(models.Model):
	contract = models.ForeignKey(Contract)
	name = models.CharField(max_length=default_length, unique=True)

	def owner(self):
		return self.contract.person

	def __unicode__(self):
		return self.name
