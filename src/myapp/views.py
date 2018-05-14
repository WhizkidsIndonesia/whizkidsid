from django.http import HttpResponse
from django.views.generic import TemplateView
from .tasks import show_hello_world


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply()
        return super().get(*args, **kwargs)


class Login(TemplateView):
    template_name = 'login.html'

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

def logged_in(request):
    return HttpResponse('OKAY!')