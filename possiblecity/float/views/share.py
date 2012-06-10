# portfolio/views/share.py

from django.views.generic import CreateView, UpdateView, DeleteView

from markdown import markdown

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template import RequestContext

from float.models import Project, ProjectImage

from float.forms import ProjectForm, ProjectImageForm

class ProjectCreateView(CreateView):
    form_class = ProjectForm
    success_url = 'success'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.slug = str(slugify(form.cleaned_data['title']))
        self.object.featured = False
        self.object.enable_comments = False
        self.object.moderate_comments = False
        self.object.status = Project.STATUS_PENDING
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ProjectCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': True})
        return context_data

class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    template_name = 'float/create_project.html'
    success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        if self.project.user.id != request.user.id:
            return HttpResponseForbidden()
        return super(ProjectUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = Project.STATUS_PENDING
        self.object.save()
        if self.object.status == Project.STATUS_PUBLISHED:
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ProjectCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': False})
        return context_data

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.project.id != project.user.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            project.status = Idea.STATUS_PENDING
            project = form.save()
            if project.status == idea.STATUS_PUBLISHED:
                return HttpResponseRedirect(project.get_absolute_url())
            else:
                return HttpResponseRedirect(reverse('profiles_profile_detail', args=[request.user]))
    else:
        form = ProjectForm(instance=project)
    context = {'project': project, 'form': form, 'add': False}
    return render_to_response('portfolio/project_form.html',
        context,
        context_instance=RequestContext(request))

class ProjectImageCreateView(CreateView):
    form_class = ProjectImageForm
    template_name = 'float/create_image.html'
    success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        return super(ProjectImageCreateView, self).dispatch(*args, **kwargs)

@login_required
def add_image(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.id != project.user.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            title = form.cleaned_data['title']
            slugified_title = str(slugify(title))
            new_image.slug = slugified_title
            new_image.public = True
            new_image.project = project.id
            new_image.save()
            form.save()
            if '_save' in request.POST:
                return HttpResponseRedirect(reverse('profiles_profile_detail',
                    args=[request.user]))
            elif '_addanother' in request.POST:
                return HttpResponseRedirect(reverse('portfolio-image-add',
                    args=[project.id]))
    else:
        form = ImageForm()
    context = {'project': project, 'form': form, 'add': True}
    return render_to_response('portfolio/image_form.html',
        context,
        context_instance=RequestContext(request))

@login_required
def edit_image(request, project_id, image_id):
    project = get_object_or_404(Project, pk=project_id)
    image = get_object_or_404(ProjectImage, pk=image_id)
    if request.user.id != project.user.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectImageForm(instance=image, data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save()
            if '_save' in request.POST:
                return HttpResponseRedirect(reverse('profiles_profile_detail',
                    args=[request.user]))
            elif '_edit' in request.POST:
                return HttpResponseRedirect(reverse('idea-edit',
                    args=[project.id]))
    else:
        form = ProjectImageForm(instance=image)
    context = {'project': project, 'form': form, 'add': False}
    return render_to_response('portfolio/image_form.html',
        context,
        context_instance=RequestContext(request))

