from django.contrib import admin
from models import Person, Product, Contract, Domain
from limeade.web.models import Limitset as WebLimitset
from limeade.mail.models import Limitset as MailLimitset
from limeade.cloud.models import Limitset as CloudLimitset
from limeade.mysql.models import Limitset as MySQLLimitset
from limeade.ftp.models import Limitset as FTPLimitset

class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'company', 'address', 'parent')
	list_display_links = ('first_name', 'last_name', 'company')
	search_fields = ['first_name', 'last_name', 'company']
	list_filter = ['parent']
	

class WebLimitsetInline(admin.StackedInline):
	model = WebLimitset

class MailLimitsetInline(admin.StackedInline):
	model = MailLimitset

class CloudLimitsetInline(admin.StackedInline):
	model = CloudLimitset

class MySQLLimitsetInline(admin.StackedInline):
	model = MySQLLimitset

class FTPLimitsetInline(admin.StackedInline):
	model = FTPLimitset

class ProductAdmin(admin.ModelAdmin):
	inlines = [
		WebLimitsetInline,
		MailLimitsetInline,
		CloudLimitsetInline,
		MySQLLimitsetInline,
		FTPLimitsetInline,
	]

class DomainInline(admin.TabularInline):
	model = Domain
	extra = 3

class DomainAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'contract')
	search_fields = ['name']

class ContractAdmin(admin.ModelAdmin):
	inlines = [DomainInline]


class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'company', 'address', 'parent')
	list_display_links = ('first_name', 'last_name', 'company')
	search_fields = ['company']
	list_filter = ['parent']

admin.site.register(Person, PersonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Domain, DomainAdmin)
