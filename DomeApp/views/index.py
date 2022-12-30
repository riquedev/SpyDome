from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "about.html"


class LoginView(TemplateView):
    template_name = "DomeApp/pages/login.html"
