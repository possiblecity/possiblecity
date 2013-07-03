# profiles/views.py

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm

class ProfileListView(ListView):
    context_object_name = "profiles"
    queryset = Profile.objects.filter(is_public=True)

class ProfileDetailView(DetailView):    
    context_object_name = "profile" 

    def get_object(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs["username"])
        profile = get_object_or_404(Profile, user=self.profile_user)
        
        #if not self.request.user.has_perm("can_view", obj=profile):
        #    raise Http404
        
        if not profile.is_public:
            if self.profile_user != self.request.user:
                profile = None
        
        return profile

    def get_context_data(self, **kwargs):
        is_current = self.request.user == self.profile_user
        
        ctx = {
            "is_current": is_current,
            "profile_user": self.profile_user,
        }
        ctx.update(super(ProfileDetailView, self).get_context_data(**kwargs))
        
        return ctx
     
class ProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    model = Profile
    template_name = "profiles/profile_create.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        self.object = profile

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.object.get_absolute_url()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = "profiles/profile_update.html"
    
    def get_object(self, queryset=None):
        profile = Profile.objects.get(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        self.object = profile
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.object.get_absolute_url()
