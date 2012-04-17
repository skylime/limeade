from django.contrib import admin
from models import VHost, PoolIP, SSLCert

admin.site.register(VHost)
admin.site.register(PoolIP)
admin.site.register(SSLCert)