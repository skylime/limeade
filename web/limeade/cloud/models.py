from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

from ..system.models import Product


default_length = 250


class Node(models.Model):
    """Creates a new node in the cloud.
    
    :param name: the name of the node
    :param uri: the unique resource identifier of the node
    """
    name     = models.CharField(max_length=default_length)
    uri      = models.CharField(max_length=default_length)
    
    def __unicode__(self):
        """Unicode representation for the node."""
        return unicode(self.name)


class Instance(models.Model):
    """Creates a cloud instance
    
    :param hostname: the hostname of the instance
    :param sshkeys: foreign key to the ssh keys
    :param owner: the owner of the instance
    :param domain: domain of the instance
    :param node: foreign key to the cloud node
    :param active: indicates if the instance is active
    :param mac_addr: the mac address of the instance
    """
    hostname = models.CharField(max_length=default_length)
    sshkeys  = models.ManyToManyField('SSHKey', blank=True)
    owner    = models.ForeignKey(User)
    domain   = models.CharField(max_length=default_length, unique=True)
    node     = models.ForeignKey(Node)
    active   = models.BooleanField(default=False)
    mac_addr = models.CharField(max_length=17, blank=True)
    
    def save(self, **kwargs):
        """Saves the instance."""
        owner = str(self.owner)
        if not self.domain:
            self.domain = owner + '-' + self.hostname.split('.')[0]
        try:
            super(Instance, self).save(**kwargs)
        except IntegrityError:
            i = 2
            base_name = self.domain
            while True:
                self.domain = base_name + '-' + str(i)
                try:
                    super(Instance, self).save(**kwargs)
                    return
                except IntegrityError:
                    i += 1
    
    def generate_mac_addr(self):
        """Creates a mac address."""
        fru = '46:52:55:'
        bar = hex(0x424152 ^ self.pk)[2:]
        self.mac_addr = fru + bar[0:2] + ':' + bar[2:4] + ':' + bar[4:6]
    
    def __unicode__(self):
        """Unicode representation for the instance."""
        return unicode(self.node) + '/' + self.domain


class SSHKey(models.Model):
    """Creates a SSH Key for the cloud instance.
    
    :param comment: comment for this key
    :param key: the ssh key
    :param owner: the owner of this key
    """
    comment = models.CharField(max_length=default_length)
    key     = models.TextField()
    owner   = models.ForeignKey(User)
    
    def __unicode__(self):
        """Unicode representation for the ssh key."""
        return self.comment


class Limitset(models.Model):
    """Maxmimum limit for an cloud instance.
    
    :param product: foreign key to the product
    :param cpu_cores: max number of cpu cores
    :param memory: max number of memory
    :param storage: max number of storage
    
    :Example:
    
        >>> from limeade.system.models import Person
        >>> person = Person.objects.get(pk=1)
        >>> person
        <Person: Test User (Test Company)>
    
    """
    product = models.ForeignKey(Product, unique=True, related_name='limitset_cloud')
    cpu_cores = models.IntegerField("Cores")
    memory    = models.IntegerField("Memory", help_text="MB")
    storage   = models.IntegerField("Storage", help_text="MB")
    
    is_limitset = True
    @staticmethod
    def utilization(user, ressource):
        """Returns the correct ressource."""
        return None
    
    class Meta:
        verbose_name = 'Cloud'

