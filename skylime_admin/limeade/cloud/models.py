from django.db import models
from django.contrib.auth.models import User
from limeade.system.models import Product
from django.db import IntegrityError

default_length = 250

class Node(models.Model):
	name     = models.CharField(max_length=default_length)
	uri      = models.CharField(max_length=default_length)

	def __unicode__(self):
		return unicode(self.name)


class Instance(models.Model):
	hostname = models.CharField(max_length=default_length)
	sshkeys  = models.ManyToManyField('SSHKey', blank=True)
	owner    = models.ForeignKey(User)
	
	domain   = models.CharField(max_length=default_length, unique=True)
	node     = models.ForeignKey(Node)

	active   = models.BooleanField(default=False)
	mac_addr = models.CharField(max_length=17, blank=True)
	
	def save(self, **kwargs):
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
		fru = '46:52:55:'
		bar = hex(0x424152 ^ self.pk)[2:]
		self.mac_addr = fru + bar[0:2] + ':' + bar[2:4] + ':' + bar[4:6]
		
	def __unicode__(self):
		return unicode(self.node) + '/' + self.domain
		

class SSHKey(models.Model):
	comment = models.CharField(max_length=default_length)
	key     = models.TextField()
	owner   = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.comment
		

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
	
