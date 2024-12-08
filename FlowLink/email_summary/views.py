import imaplib
import email
from email.header import decode_header
import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from social_django.utils import psa
from django.conf import settings
from django.http import HttpResponse
from pathlib import Path

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

def excel_view(request):
    emails = []
    data_extracted = False
    if request.method == 'POST':
        # Connect to the Gmail server
        mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
        mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        mail.select("inbox")

        # Fetch only the latest 100 emails
        result, data = mail.search(None, "ALL")
        email_ids = data[0].split()[-100:]

        emails_list = []

        for eid in email_ids:
            result, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Decode email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Get email from and date
            from_ = msg.get("From")
            date_ = msg.get("Date")
            
            emails_list.append({"subject": subject, "from": from_, "date": date_})

        # Convert emails list to a DataFrame and save to JSON
        df = pd.DataFrame(emails_list)
        json_file_path = Path(settings.BASE_DIR) / 'emails_data.json'
        df.to_json(json_file_path, orient='records')

        request.session['emails_data_path'] = str(json_file_path)
        emails = emails_list
        data_extracted = True

    return render(request, 'emails/excel.html', {'emails': emails, 'data_extracted': data_extracted})

def download_json(request):
    json_file_path = request.session.get('emails_data_path')
    if not json_file_path:
        return redirect('excel_view')

    with open(json_file_path, 'r') as f:
        data = f.read()
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="emails_data.json"'
    return response

def download_csv(request):
    json_file_path = request.session.get('emails_data_path')
    if not json_file_path:
        return redirect('excel_view')

    with open(json_file_path, 'r') as f:
        emails = json.load(f)

    df = pd.DataFrame(emails)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails_data.csv"'
    df.to_csv(path_or_buf=response, index=False)
    
    return response
