from django.db import models
from limeade.system.models import Product
from limeade.system.utils import get_domains, md5crypt, gen_salt
from limeade.web.models import VHost, get_vhosts
from django.db import IntegrityError

default_length = 250

class Account(models.Model):
	name     = models.CharField(max_length=default_length, unique=True)
	password = models.CharField(max_length=default_length)
	vhost    = models.ForeignKey(VHost)
	
	def set_password(self, password):
		self.password = md5crypt(password, gen_salt())
	
	def save(self, **kwargs):
		owner = str(self.vhost.domain.owner())
		if not self.name.startswith(owner + '_'):
			self.name = owner + '_' + self.name
		try:
			super(Account, self).save(**kwargs)
		except IntegrityError:
			i = 1
			base_name = self.name
			while True:
				self.name = base_name + '-' + str(i)
				try:
					super(Account, self).save(**kwargs)
					return
				except IntegrityError:
					i += 1
				
	def __unicode__(self):
		return unicode(self.name) + '@' + unicode(self.vhost)

		
class Limitset(models.Model):
	product = models.ForeignKey(Product, unique=True, related_name='limitset_ftp')
	accounts = models.IntegerField("Accounts")

	is_limitset = True
	@staticmethod
	def utilization(user, ressource):
		if ressource == 'accounts':
			return Account.objects.filter(vhost__in=list(get_vhosts(user))).count()
		return None
		
	class Meta:
		verbose_name = 'FTP'
