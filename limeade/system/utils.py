from django.db.models.query import CollectedObjects
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from models import Product, Contract, Domain

def get_domains(user):
	contracts = user.contract_set.values_list('pk', flat=True)
	return Domain.objects.filter(contract__in=list(contracts))
	
	
def get_limitsets():
	return [r for r in Product._meta.get_all_related_objects() if hasattr(r.model, 'is_limitset')]
	
