from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ..cloud.models import Limitset as CloudLimitset
from ..mysql.models import Limitset as MySQLLimitset
from ..mail.models import Limitset as MailLimitset
from ..web.models import Limitset as WebLimitset
from ..ftp.models import Limitset as FTPLimitset
from .models import Person
from .models import Product
from .models import Contract
from .models import Domain


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'address', 'parent',)
    list_display_links = ('first_name', 'last_name', 'company',)
    search_fields = ['first_name', 'last_name', 'company',]
    list_filter = ['parent',]


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
    list_display = ('name', 'owner', 'contract',)
    search_fields = ['name',]


class ContractAdmin(admin.ModelAdmin):
    inlines = [DomainInline,]


admin.site.register(Person, PersonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Domain, DomainAdmin)

