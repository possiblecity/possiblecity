# float/views/explore.py

from django.views.generic import TemplateView, DetailView, ListView

from ..models import Project

class ExploreView(DetailView):
    pass

class ProjectDetailView(DetailView):
    model = Project

class ProjectListView(ListView):
    model = Project
