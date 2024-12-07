import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.core.management.base import BaseCommand
from emails.models import Email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Command(BaseCommand):
    help = 'Fetch emails from the configured email server'

    def handle(self, *args, **kwargs):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])

        for msg in messages:
            msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = msg.get('payload', {})
            headers = payload.get('headers', [])
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            summary = payload.get('body', {}).get('data', '')

            Email.objects.create(
                sender_name=sender,
                sender_email=sender,
                subject=subject,
                summary=summary,
                date_received=msg['internalDate']
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched emails'))
