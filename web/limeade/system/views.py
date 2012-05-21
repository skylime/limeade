from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import update_object
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Count
from django.template import RequestContext

from .models import Person
from .models import Product
from .models import Contract
from .models import Domain
from .forms import PersonForm
from .forms import PersonAddForm
from .forms import ProductForm
from .forms import ContractForm
from .forms import DomainForm
from .utils import get_limitsets
#from limeade.mail.models import Limitset as MailLimitset


@login_required
def ressources(request):
    limits = {}
    for limitset in get_limitsets():
        prefix = 'product__' + limitset.get_accessor_name()
        
        # has the user any contract with this limitset?
        if request.user.contract_set.aggregate(Count(prefix))[prefix + '__count'] < 1: continue
        limits[limitset.model._meta.verbose_name] = []
        
        for field in limitset.model._meta.fields:
            if field.primary_key: continue
            if field.name == 'product': continue
            key = prefix + '__' + field.name
            limits[limitset.model._meta.verbose_name] += [{
                'name': field.verbose_name,
                'help_text': field.help_text,
                'utilization': limitset.model.utilization(request.user, field.name),
                'value': request.user.contract_set.aggregate(Sum(key))[key + '__sum']
            }]
    
    return render_to_response('limeade_system/ressources.html',
        {'limits': limits}, context_instance = RequestContext(request))


@login_required
def account(request):
    return render_to_response(
        'limeade_system/account.html',
        {'person': request.user.get_profile()},
        context_instance = RequestContext(request)
    )


@permission_required('system.reseller')
def customer_list(request):
    return object_list(request, Person.objects.filter(parent=request.user), template_name='limeade_system/customer_list.html')


@permission_required('system.reseller')
def customer_add(request):
    # TODO: check username is uniqe
    form = PersonAddForm(request.POST or None)
    if form.is_valid():
        username   = form.cleaned_data['username']
        email      = form.cleaned_data['email']
        password   = form.cleaned_data['last_name']
        first_name = form.cleaned_data['first_name']
        last_name  = form.cleaned_data['last_name']
        company    = form.cleaned_data['company']
        address    = form.cleaned_data['address']
        u = User(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name)
        u.save()
        p = Person(user=u, company=company, address=address, parent=request.user.get_profile())
        p.save()
        return redirect('limeade_system_customer_view', username)
    return render_to_response(
        'limeade_system/customer_add.html',
        {'form': form},
        context_instance = RequestContext(request)
    )


@permission_required('system.reseller')
def customer_view(request, slug):
    u = get_object_or_404(User, username = slug)
    c = Contract.objects.filter(person=u.person)
    return object_detail(
        request,
        Person.objects.all(),
        slug = slug,
        slug_field = 'user__username',
        extra_context = {
            'contracts': c,
        },
        template_name='limeade_system/customer_view.html'
    )


@permission_required('system.reseller')
def customer_edit(request, slug):
    # TODO: check username is uniqe
    # TODO: permissions, permissions permissions!
    u = get_object_or_404(User, username = slug)
    p = u.person
    data = {
        'first_name': u.first_name,
        'last_name':  u.last_name,
        'company':    p.company,
        'address':    p.address,
        'email':      u.email,
        
    }
    form = PersonForm(request.POST or data)
    if form.is_valid() and request.POST:
        u.email      = form.cleaned_data['email']
        u.first_name = form.cleaned_data['first_name']
        u.last_name  = form.cleaned_data['last_name']
        p.company    = form.cleaned_data['company']
        p.address    = form.cleaned_data['address']
        u.save()
        p.save()
        return redirect('limeade_system_customer_view', u.username)
    return render_to_response(
        'limeade_system/customer_edit.html',
        {'form': form, 'username': u.username},
        context_instance = RequestContext(request)
    )


@permission_required('system.reseller')
def customer_delete(request, slug):
    # TODO: permission checking
    get_object_or_404(Person, user__username = slug).delete()
    return redirect('limeade_system_customer_list')


@permission_required('system.reseller')
def customer_manage(request, slug):
    new_user = get_object_or_404(User, username = slug)
    # TODO: permission checking
    original_user = request.user.username
    new_user.backend = 'django.contrib.auth.backends.ModelBackend' 
    login(request, new_user)
    request.session['limeade_original_user'] = original_user
    return redirect(ressources)


@login_required
def customer_manage_return(request):
    original_user = User.objects.filter(username=request.session['limeade_original_user'])[0]
    original_user.backend = 'django.contrib.auth.backends.ModelBackend' 
    login(request, original_user)
    return redirect(ressources)


@permission_required('system.reseller')
def contract_add(request, slug):
    u = get_object_or_404(User, username = slug)
    form = ContractForm(request.POST or None)
    form.fields['product'].queryset = Product.objects.filter(owner=request.user)
    if form.is_valid():
        c = form.save(commit=False)
        c.person = u
        c.save()
        return redirect('limeade_system_customer_view', slug = u)
    return render_to_response("limeade_system/contract_add.html",
        {"form": form}, context_instance = RequestContext(request))


@permission_required('system.reseller')
def contract_customize(request, slug, contract_id):
    u = get_object_or_404(User, username = slug)
    c = get_object_or_404(Contract, pk = contract_id)
    p = c.product
        
    form = ProductForm(request.POST or None, instance=p)
    
    limitsets = []
    for limitset in get_limitsets():
        LimitInlineFormSet = inlineformset_factory(Product, limitset.model, can_delete=False)
        limitsets += [LimitInlineFormSet(request.POST or None, instance=p)]
        # workaround, as templates can't access private members
        limitsets[-1].verbose_name = limitsets[-1].model._meta.verbose_name
    
    if form.is_valid() and all([x.is_valid() for x in limitsets]):
        if not p.personalized:
            p.id = None
            p.personalized = True
        p = form.save()
        c.product = p
        c.save()
        for l in limitsets:
            data = l.forms[0].cleaned_data
            data.pop('id')
            data['product'] = p
            l.model(**data).save()
        return redirect('limeade_system_customer_view', slug = slug)
    return render_to_response("limeade_system/product_edit.html",
        {"form": form, "limitsets": limitsets}, context_instance = RequestContext(request))


@permission_required('system.reseller')
def contract_delete(request, slug, contract_id):
    c = get_object_or_404(Contract, pk = contract_id)
    if c.person.get_profile().parent != request.user:
        return redirect_to_login(reverse(contract_delete))
    c.delete()
    return redirect('limeade_system_customer_view', slug = slug)


def domain_add(request, slug, contract_id):
    u = get_object_or_404(User, username = slug)
    c = get_object_or_404(Contract, pk = contract_id)
    form = DomainForm(request.POST or None)
    if form.is_valid():
        d = form.save(commit=False)
        d.contract = c
        d.save()
        return redirect('limeade_system_customer_view', slug = slug)
    return render_to_response("limeade_system/domain_add.html",
        {"form": form}, context_instance = RequestContext(request))


def domain_delete(request, slug, contract_id, domain_id):
    # TODO: permission checks
    get_object_or_404(Domain, pk = domain_id).delete()
    # TODO: cleanup related objects
    return redirect('limeade_system_customer_view', slug = slug)


@permission_required('system.reseller')
def product_list(request):
    return object_list(request, Product.objects.filter(owner=request.user), template_name='limeade_system/product_list.html')


@permission_required('system.reseller')
def product_add(request):
    form = ProductForm(request.POST or None)
    p = None
    if form.is_valid():
        p = form.save(commit=False)
        p.owner = request.user
    
    limitsets = []
    for limitset in get_limitsets():
        LimitInlineFormSet = inlineformset_factory(Product, limitset.model, can_delete=False)
        limitsets += [LimitInlineFormSet(request.POST or None, instance=p)]
        # workaround, as templates can't access private members
        limitsets[-1].verbose_name = limitsets[-1].model._meta.verbose_name
    
    if form.is_valid() and all([x.is_valid() for x in limitsets]):
        form.save()
        for l in limitsets:
            l.save()
        return redirect('limeade_system_product_list')
    return render_to_response("limeade_system/product_add.html",
        {"form": form, "limitsets": limitsets}, context_instance = RequestContext(request))


@permission_required('system.reseller')
def product_edit(request, slug, next='limeade_system_product_list'):
    p = Product.objects.get(pk=slug)
    form = ProductForm(request.POST or None, instance=p)
    
    limitsets = []
    for limitset in get_limitsets():
        LimitInlineFormSet = inlineformset_factory(Product, limitset.model, can_delete=False)
        limitsets += [LimitInlineFormSet(request.POST or None, instance=p)]
        # workaround, as templates can't access private members
        limitsets[-1].verbose_name = limitsets[-1].model._meta.verbose_name
    
    if form.is_valid() and all([x.is_valid() for x in limitsets]):
        form.save()
        for l in limitsets:
            l.save()
        return redirect(next)
    return render_to_response("limeade_system/product_edit.html",
        {"form": form, "limitsets": limitsets}, context_instance = RequestContext(request))


@permission_required('system.reseller')
def product_delete(request, slug):
    get_object_or_404(Product, pk = slug).delete()
    return redirect('limeade_system_product_list')

