# ideas/views/share.py

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from ..models import Idea, IdeaVisual
from ..forms import IdeaForm, IdeaVisualForm, SimpleIdeaForm

class IdeaCreateView(LoginRequiredMixin, CreateView):
    form_class = SimpleIdeaForm
    template_name = 'ideas/idea_create.html'
    success_url = reverse_lazy('ideas_idea_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.slug = str(slugify(form.cleaned_data['tagline']))
        self.object.featured = False
        self.object.enable_comments = True
        self.object.moderate_comments = False
        self.object.status = Idea.STATUS_PUBLISHED
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(IdeaCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': True})
        return context_data

class IdeaUpdateView(LoginRequiredMixin, UpdateView):
    form_class = IdeaForm
    template_name = 'ideas/idea_update_form.html'
    #success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.idea = get_object_or_404(Idea, pk=kwargs['idea_id'])
        if self.idea.user.id != request.user.id:
            return HttpResponseForbidden()
        return super(IdeaUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = Idea.STATUS_PENDING
        self.object.save()
        if self.object.status == Idea.STATUS_PUBLISHED:
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(IdeaCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': False})
        return context_data


class IdeaVisualCreateView(CreateView):
    form_class = IdeaVisualForm
    #template_name = 'float/create_image.html'
    #success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.idea = get_object_or_404(Idea, pk=kwargs['idea_id'])
        return super(IdeaVisualCreateView, self).dispatch(*args, **kwargs)

