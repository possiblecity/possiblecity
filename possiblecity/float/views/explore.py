# float/views/explore.py

from django.views.generic import TemplateView, DetailView, ListView

from float.models import Project

class ExploreView(DetailView):
    pass

class ProjectDetailView(DetailView):
    model = Project

class ProjectListView(ListView):
    queryset = Project._default_manager.filter(status=Project.STATUS_LIVE).order_by('-featured', '-date_end')
    paginate_by = settings.PROJECT_PAGINATE_BY