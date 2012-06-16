import account.forms
import account.views


class LoginView(account.views.LoginView):
    # override the default account login form to use email address as username
    form_class = account.forms.LoginEmailForm