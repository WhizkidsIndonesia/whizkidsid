from __future__ import print_function

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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

def index(request):
    if not request.user.is_authenticated():
        form = SignUpForm()
        return render(request, 'home.html', {'form': form})
    else:
        return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.username = user.email.split("@")[0]
            user.refresh_from_db()
            user.is_active = False
            user.save()
            subject = 'Konfirmasi pendaftaran Anda di Whizkids.id'
            message = render_to_string('account_activation_email.html', {
                'username': user.email.split("@")[0],
                'user': user,
                'host': 'whizkids.id', #request.get_host(), #TOFIX for docker container
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #TODO background
            send_message(user.email, subject, message, message)
            messages.info(request, 'Silahkan cek email pendaftaran yang baru saja kami kirimkan ke %s' % user.email)
            return redirect('index')


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
        messages.info(request, 'Akun berhasil di aktifkan! Selamat datang di Whizkids Indonesia!')
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
def member(request):
    return render(request, 'member.html')
    # return render(request, 'isoworld/Isometric Game.html')

@login_required
def world(request):
    return render(request, 'isoworld/Isometric Game.html')