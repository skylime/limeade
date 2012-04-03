from django.db import models

default_length = 250


class Service(models.Model):
	name = models.CharField(max_length=default_length, unique=True)
	
	def __unicode__(self):
		return unicode(self.name)
	

class Server(models.Model):
	hostname = models.CharField(max_length=default_length, unique=True)
	ip       = models.CharField(max_length=default_length, unique=True)
	services = models.ManyToManyField(Service)
	enabled  = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.hostname)
