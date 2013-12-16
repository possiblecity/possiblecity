# possiblecity/views.py 

from django.views.generic.list import ListView

from actstream.models import Action

from apps.ideas.models import Idea

class HomepageView(ListView):    
    queryset = Idea.objects.filter(featured=True)[:8]
    context_object = "ideas"
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        
        ctx = {
            "activity_stream": Action.objects.filter(public=True)[:8]
        }

        ctx.update(super(HomePageView, self).get_context_data(**kwargs))
        
        return ctx