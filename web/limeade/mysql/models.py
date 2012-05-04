from django.db import models
from limeade.system.models import Product, Domain

default_length = 250

class Limitset(models.Model):
	product = models.ForeignKey(Product, unique=True, related_name='limitset_mysql')
	dbs     = models.IntegerField("MySQL Databases")


	is_limitset = True
	@staticmethod
	def utilization(user, ressource):
		# todo
		# MAX_QUERIES_PER_HOUR
		# MAX_UPDATES_PER_HOUR
		# MAX_CONNECTIONS_PER_HOUR
		# MAX_USER_CONNECTIONS
		return None
		
	class Meta:
		verbose_name = 'MySQL'
