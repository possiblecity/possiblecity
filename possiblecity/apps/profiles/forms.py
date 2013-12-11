import floppyforms as forms
from django.contrib.auth.models import User

from .models import Profile


class SimpleFileInput(forms.ClearableFileInput):
    template_name = 'floppyforms/widgets/bootstrap_file.html'

class TwitterTextInput(forms.TextInput):
    template_name = 'floppyforms/widgets/twitter.html'

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'about', 'photo', 'phone', 'website', 'twitter')
        widgets = {
            'about': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Not publicly displayed'}),
            'website': forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Include http://'}),
            #'twitter': TwitterTextInput(),
            'twitter': forms.TextInput(attrs={'class':'form-control'}),
            'photo': SimpleFileInput(),
        }
        

    def save(self, *args, **kwargs):
        """
        Update the first name and last name on the related User object. 
        """
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile
