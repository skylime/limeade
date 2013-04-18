"""Models for limeade cluster"""
from django.db import models
from macaddress.fields import *

default_length = 250


class Service(models.Model):
    """Creates a cluster service.
    
    :param name: name of the service
    """
    name = models.CharField(max_length=default_length, unique=True)
    
    def __unicode__(self):
        """Unicode representation for the service."""
        return unicode(self.name)


class Region(models.Model):
    """Creates a cluster region.
    
    :param name: name of the region
    """
    name = models.CharField(max_length=default_length, unique=True)
    
    def __unicode__(self):
        """Unicode representation for the region."""
        return unicode(self.name)


class Server(models.Model):
    """Creates a cluster server.
    
    :param hostname: name of the region
    :param ip: the ip of the server
    :param region: foreign key to cluster region
    :param services: foreign key to cluster service
    :param enabled: indicates if this server is enabled
    """
    hostname = models.CharField(max_length=default_length, unique=True)
    ip       = models.GenericIPAddressField(unique=True)
    mac      = MACAddressField(unique=True)
    region   = models.ForeignKey(Region)
    services = models.ManyToManyField(Service)
    enabled  = models.BooleanField(default=False)

    def __unicode__(self):
        """Unicode representation for the server."""
        return unicode(self.hostname)

