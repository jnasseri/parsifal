# coding: utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from reviews.models import Review
from parsifal_auth.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'There was some problems while creating your account. Please review some fields before submiting again.')
            context = RequestContext(request, {'form': form})
            return render_to_response('auth/signup.html', context)
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your account were successfully created.')
            return HttpResponseRedirect('/' + username + '/')
    else:
        context = RequestContext(request,  {'form': SignUpForm() })
        return render_to_response('auth/signup.html', context)

def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.GET['next'])
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages.add_message(request, messages.ERROR, 'Your account is desactivated.')
                    context = RequestContext(request)
                    return render_to_response('auth/signin.html', context)
            else:
                messages.add_message(request, messages.ERROR, 'Username or password invalid.')
                context = RequestContext(request)
                return render_to_response('auth/signin.html', context)
        else:
            context = RequestContext(request)
            return render_to_response('auth/signin.html', context)

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def reset(request):
    return password_reset(request, template_name='auth/reset.html',
        email_template_name='auth/reset_email.html',
        subject_template_name='auth/reset_subject.txt',
        post_reset_redirect=reverse('success'))

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='auth/reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('signin'))

def success(request):
  return render(request, "auth/success.html")
