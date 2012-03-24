from django.db import models

default_length = 250

class Server(models.Model):
	hostname = models.CharField(max_length=default_length, unique=True)
	ip       = models.CharField(max_length=default_length, unique=True)
	services = models.ManyToManyField(Service)

	def __unicode__(self):
		return unicode(self.hostname)


class Service(models.Model):
	name = models.CharField(max_length=default_length, unique=True)