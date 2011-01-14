from django.db import models
from django.contrib.auth.models import User
from limeade.system.models import Product

default_length = 250

class Node(models.Model):
	name     = models.CharField(max_length=default_length)
	uri      = models.CharField(max_length=default_length)

	def __unicode__(self):
		return unicode(self.name)


class Instance(models.Model):
	name   = models.CharField(max_length=default_length)
	node   = models.ForeignKey(Node)
	owner  = models.ForeignKey(User)
	active = models.BooleanField(default=False)
	
	def domain(self):
		return self.owner.username + '-' + self.name
		
	def __unicode__(self):
		return unicode(self.node) + '/' + self.name
	
	class Meta:
		unique_together = (("owner", "name"),)
		


class Limitset(models.Model):
	product = models.ForeignKey(Product, unique=True, related_name='limitset_cloud')
	cpu_cores = models.IntegerField("Cores")
	memory    = models.IntegerField("Memory", help_text="MB")
	storage   = models.IntegerField("Storage", help_text="MB")

	is_limitset = True
	@staticmethod
	def utilization(user, ressource):
		return None
		
	class Meta:
		verbose_name = 'Cloud'
	
