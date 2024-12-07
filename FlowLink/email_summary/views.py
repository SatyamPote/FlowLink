from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from social_django.utils import psa
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64
import requests
from emails.models import Email

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@psa('social:complete')
def authorize(request, backend):
    user = request.backend.do_auth(request.GET.get('code'))
    if user:
        auth_login(request, user)
        return redirect('dashboard')
    return redirect('login')

def email_list(request):
    emails = Email.objects.all()
    return render(request, 'emails/index.html', {'emails': emails})

def email_detail(request, email_id):
    email = get_object_or_404(Email, pk=email_id)
    return render(request, 'emails/email_detail.html', {'email': email})

def github_dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    social = user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    headers = {'Authorization': f'token {token}'}

    prs_url = 'https://api.github.com/user/pulls'
    prs_response = requests.get(prs_url, headers=headers)
    prs_data = prs_response.json()

    context = {
        'pull_requests': prs_data,
    }
    return render(request, 'github_dashboard.html', context)

def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        data = pd.read_excel(excel_file)

        # Save to session or process data immediately
        request.session['excel_data'] = data.to_dict()

        return redirect('excel_summary')

    return render(request, 'upload_excel.html')

def excel_summary(request):
    data = pd.DataFrame(request.session.get('excel_data'))
    summary = data.describe().to_html()

    # Create a simple plot
    plt.figure()
    data.plot(kind='bar')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    context = {
        'summary': summary,
        'plot_url': plot_url,
    }
    return render(request, 'excel_summary.html', context)
