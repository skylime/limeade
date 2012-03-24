from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext


from models import Server, Service
from forms import ServerForm

@login_required
def server_list(request):
	return object_list(request, Server),
			template_name='limeade_cluster/server_list.html')

@login_required
def server_add(request):
	form = ServerForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('limeade_cluster_server_list')
	return render_to_response("limeade_cluster/server_add.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required	
def server_edit(request, slug):
	server = Server.objects.get(pk=slug)
	form = ServerForm(request.POST or None, instance=server)
	if form.is_valid():
		form.save()
		return redirect('limeade_cluster_server_list')
	return render_to_response("limeade_cluster/server_edit.html",
		{"form": form}, context_instance = RequestContext(request))

@login_required
def server_delete(request, slug):
	s = get_object_or_404(Server, pk = slug)
	s.delete()
	return redirect('limeade_cluster_server_list')
	
