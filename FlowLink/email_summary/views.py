import os
import shutil
import imaplib
import email
from email.header import decode_header
import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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

def file_organizer_view(request):
    if request.method == 'POST':
        directory = request.POST.get('directory')
        if not os.path.isdir(directory):
            return render(request, 'file_organizer.html', {'error': 'Invalid directory'})

        extensions = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Audio': ['.mp3', '.wav', '.aac'],
            'Video': ['.mp4', '.avi', '.mkv'],
            'Archives': ['.zip', '.rar', '.tar'],
            'Others': []
        }

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                moved = False
                for folder, exts in extensions.items():
                    if file_ext in exts:
                        folder_path = os.path.join(directory, folder)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        shutil.move(file_path, os.path.join(folder_path, filename))
                        moved = True
                        break
                if not moved:
                    other_folder_path = os.path.join(directory, 'Others')
                    if not os.path.exists(other_folder_path):
                        os.makedirs(other_folder_path)
                    shutil.move(file_path, os.path.join(other_folder_path, filename))

        return render(request, 'file_organizer.html', {'success': 'Files organized successfully!'})

    return render(request, 'file_organizer.html')
