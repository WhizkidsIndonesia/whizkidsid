from __future__ import print_function

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from myapp.forms import SignUpForm
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def email(request):

    import os
    from apiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools
    # Setup the Gmail API
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()

    if not creds or creds.invalid:

        flow = client.flow_from_clientsecrets(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json'), SCOPES)
        print('bisa?', flush=True)


        creds = tools.run_flow(flow, store)


    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    return HttpResponse('oi')
