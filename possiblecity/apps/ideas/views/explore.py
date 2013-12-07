# ideas/views/explore.py

from django.views.generic import TemplateView, DetailView, ListView

from ..models import Idea

class ExploreView(DetailView):
    pass

class IdeaDetailView(DetailView):
    model = Idea
    context_object_name = "idea"

class IdeaListView(ListView):
    queryset = Idea.objects.all().select_related()
    context_object_name = "ideas"

class IdeaListWithinFeature(IdeaListView):
    """
    Get all lots within a certain neighborhood
    """
    pass

class IdeaListFeaturedView(IdeaListView):
	"""
	Get all featured ideas
	"""
	queryset = Idea.objects.filter(featured=True)
