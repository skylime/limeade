from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from celery.execute import send_task
from celery.exceptions import TimeoutError
from django.contrib import messages
from forms import DBForm, DBEditForm
import re

@login_required
def db_list(request):
	try:
		dbs = send_task("mysql.list_dbs", kwargs={'user': request.user.username},routing_key='limeade.mysql').get(timeout=5)
	except TimeoutError:
		dbs = []
		messages.add_message(request, messages.ERROR, 'Backend not responding. Please try again later.')
		
	return render_to_response("limeade_mysql/db_list.html",
		{"object_list": dbs}, context_instance = RequestContext(request))

@login_required
def db_add(request):
	form = DBForm(request.POST or None)
	if form.is_valid():
		send_task("mysql.create_db", kwargs={
				'user':     request.user.username,
				'name':     form.cleaned_data['name'],
				'password': form.cleaned_data['password'],
			}, routing_key='limeade.mysql')
		return redirect('limeade_mysql_db_list')
	return render_to_response("limeade_mysql/db_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def db_edit(request, slug):
	form = DBEditForm(request.POST or None)
	if form.is_valid():
		send_task("mysql.edit_db", kwargs={
				'user':     request.user.username,
				'name':     slug,
				'password': form.cleaned_data['password'],
			}, routing_key='limeade.mysql')
		return redirect('limeade_mysql_db_list')
	return render_to_response("limeade_mysql/db_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def db_delete(request, slug):
	if not re.match(r'[a-zA-Z0-9-]+$', slug):
		return redirect('limeade_mysql_db_list')
		
	send_task("mysql.delete_db", kwargs={
			'user':     request.user.username,
			'name':     slug,
		}, routing_key='limeade.mysql')
	return redirect('limeade_mysql_db_list')
	
