from django.conf.urls.defaults import *

from .export import user_export


urlpatterns = patterns('limeade.system.views',
    url(r'^$', 'ressources'),
    url(r'^account/$', 'account'),
    url(r'^customer/$',                        'customer_list',   name='limeade_system_customer_list'),
    url(r'^customer/add/$',                    'customer_add',    name='limeade_system_customer_add'),
    url(r'^customer/(?P<slug>[^/]+)/$',        'customer_view',   name='limeade_system_customer_view'),
    url(r'^customer/(?P<slug>[^/]+)/edit/$',   'customer_edit',   name='limeade_system_customer_edit'),
    url(r'^customer/(?P<slug>[^/]+)/delete/$', 'customer_delete', name='limeade_system_customer_delete'),
    url(r'^customer/(?P<slug>[^/]+)/manage/$', 'customer_manage', name='limeade_system_customer_manage'),
    url(r'^customer/manage/return/$', 'customer_manage_return',   name='limeade_system_manage_return'),
    url(r'^customer/(?P<slug>[^/]+)/contract/add/$',                              'contract_add',       name='limeade_system_contract_add'),
    url(r'^customer/(?P<slug>[^/]+)/contract/(?P<contract_id>[^/]+)/customize/$', 'contract_customize', name='limeade_system_contract_customize'),
    url(r'^customer/(?P<slug>[^/]+)/contract/(?P<contract_id>[^/]+)/delete/$',    'contract_delete',    name='limeade_system_contract_delete'),
    url(r'^customer/(?P<slug>[^/]+)/contract/(?P<contract_id>[^/]+)/domain/add/$',    'domain_add',     name='limeade_system_domain_add'),
    url(r'^customer/(?P<slug>[^/]+)/contract/(?P<contract_id>[^/]+)/domain/(?P<domain_id>[^/]+)/delete/$', 'domain_delete',  name='limeade_system_domain_delete'),
    #url(r'^reseller/$',                      'reseller_list'),
    #url(r'^reseller/add/$',                  'reseller_add'),
    #url(r'^reseller/(?P<id>[^/]+)/$',        'reseller_edit'),
    #url(r'^reseller/(?P<id>[^/]+)/delete/$', 'reseller_delete'),
    url(r'^product/$',                         'product_list',   name='limeade_system_product_list'),
    url(r'^product/add/$',                     'product_add',    name='limeade_system_product_add'),
    url(r'^product/(?P<slug>[^/]+)/$',         'product_edit',   name='limeade_system_product_edit'),
    url(r'^product/(?P<slug>[^/]+)/delete/$',  'product_delete', name='limeade_system_product_delete'),
)

urlpatterns += patterns('',
    url(r'^export/user.pp',  user_export),
)
