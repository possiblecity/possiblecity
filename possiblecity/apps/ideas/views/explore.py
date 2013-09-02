# ideas/views/explore.py

from django.views.generic import TemplateView, DetailView, ListView

from ..models import Idea

class ExploreView(DetailView):
    pass

class IdeaDetailView(DetailView):
    model = Idea
    context_object_name = "idea"

class IdeaListView(ListView):
    model = Idea
    context_object_name = "ideas"

class IdeaListWithinFeature(IdeaListView):
    """
    Get all lots within a certain neighborhood
    """
    pass