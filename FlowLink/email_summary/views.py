import imaplib
import email
from email.header import decode_header
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from social_django.utils import psa
from django.conf import settings
from django.http import HttpResponse

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

def extract_emails(request):
    # Connect to the Gmail server
    mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
    mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    mail.select("inbox")

    # Fetch only the latest 100 emails
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()[-100:]

    emails = []

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
        
        emails.append({"subject": subject, "from": from_, "date": date_})

        # Batch processing: if emails list reaches 20, process them
        if len(emails) % 20 == 0:
            save_emails_to_session(request, emails)
            emails = []

    # Process any remaining emails
    if emails:
        save_emails_to_session(request, emails)

    return render(request, 'emails/extract_emails.html', {'emails': request.session.get('emails_data')})

def save_emails_to_session(request, emails):
    existing_emails = request.session.get('emails_data', [])
    existing_emails.extend(emails)
    request.session['emails_data'] = existing_emails

def excel_summary(request):
    emails = request.session.get('emails_data')
    return render(request, 'emails/excel_summary.html', {'emails': emails})

def download_csv(request):
    emails = request.session.get('emails_data')
    if not emails:
        return redirect('extract_emails')
    
    df = pd.DataFrame(emails)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails_summary.csv"'
    df.to_csv(path_or_buf=response, index=False)
    
    return response
