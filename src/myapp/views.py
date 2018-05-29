from __future__ import print_function

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

from myapp.management.commands.email import send_message
from myapp.tokens import account_activation_token

from myapp.forms import SignUpForm
# from .tasks import show_hello_world

def home(request):
    if not request.user.is_authenticated():
        form = SignUpForm()
        return render(request, 'home.html', {'form': form})
    else:
        return render(request, 'home.html')

class Login(TemplateView):
    template_name = 'login.html'

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

def logged_in(request):
    return HttpResponse('OKAY!')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.username = user.email.split("@")[0]
            user.refresh_from_db()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Konfirmasi pendaftaran Anda di Whizkids.id'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #TODO background
            send_message(user.email, subject, message, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')