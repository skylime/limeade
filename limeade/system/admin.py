from django.contrib import admin
from models import Person, Product, Contract, Domain
from limeade.mail.models import Limitset as MailLimitset

class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'company', 'address', 'parent')
	list_display_links = ('first_name', 'last_name', 'company')
	search_fields = ['first_name', 'last_name', 'company']
	list_filter = ['parent']
	

class MailLimitsetInline(admin.StackedInline):
        model = MailLimitset


class ProductAdmin(admin.ModelAdmin):
        inlines = [
                MailLimitsetInline,
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
