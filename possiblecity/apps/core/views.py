# possiblecity/views.py 

from django.views.generic import TemplateView

from actstream.models import Action

from apps.ideas.models import Idea

class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomepageView, self).get_context_data(**kwargs)
        extra_context = {
            'featured_ideas': Idea.objects.filter(featured=True)[:3],
            'idea': Idea.objects.filter(featured=True).order_by('?')[0],
            'activity_stream': Action.objects.filter(public=True)[:8]
        }

        context.update(extra_context)
        
        return context