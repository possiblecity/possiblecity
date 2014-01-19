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
<<<<<<< HEAD
from ..forms import IdeaForm, IdeaVisualForm
=======
from ..forms import IdeaForm, IdeaVisualForm, SimpleIdeaForm
from ..signals import idea_created, idea_updated
>>>>>>> master

class IdeaCreateView(LoginRequiredMixin, CreateView):
    form_class = IdeaForm
    template_name = 'ideas/idea_create.html'
    success_url = reverse_lazy('ideas_idea_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        if self.object.title:
            self.object.slug = str(slugify(form.cleaned_data['title']))
        else:
            self.object.slug = str(slugify(form.cleaned_data['tagline']))
        self.object.featured = False
        self.object.enable_comments = True
        self.object.moderate_comments = False
        self.object.status = Idea.STATUS_PUBLISHED
        self.object.save()
<<<<<<< HEAD
        form.save_m2m()
        if self.object.status == Idea.STATUS_PUBLISHED:
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return HttpResponseRedirect(self.get_success_url())
=======
        idea_created.send(sender=self, idea=self.object, request=self.request)
        return HttpResponseRedirect(self.get_success_url())
>>>>>>> master

    def get_context_data(self, *args, **kwargs):
        context_data = super(IdeaCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': True})
        return context_data

class IdeaUpdateView(LoginRequiredMixin, UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'ideas/idea_update.html'
    success_url = reverse_lazy('ideas_idea_list')


    def dispatch(self, *args, **kwargs):
        self.idea = get_object_or_404(Idea, pk=kwargs['pk'])
        if self.idea.user.id != self.request.user.id and not self.request.user.is_staff:
            return HttpResponseForbidden()
        return super(IdeaUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = Idea.STATUS_PUBLISHED
        self.object.save()
<<<<<<< HEAD
        form.save_m2m()
=======
        idea_updated.send(sender=self, idea=self.object, request=self.request)
>>>>>>> master
        if self.object.status == Idea.STATUS_PUBLISHED:
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class IdeaVisualCreateView(CreateView):
    form_class = IdeaVisualForm
    #template_name = 'float/create_image.html'
    #success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.idea = get_object_or_404(Idea, pk=kwargs['idea_id'])
        return super(IdeaVisualCreateView, self).dispatch(*args, **kwargs)

