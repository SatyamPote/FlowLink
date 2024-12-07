from django.shortcuts import render, get_object_or_404
from .models import Email

def email_list(request):
    emails = Email.objects.all()
    return render(request, 'emails/index.html', {'emails': emails})

def email_detail(request, email_id):
    email = get_object_or_404(Email, pk=email_id)
    return render(request, 'emails/email_detail.html', {'email': email})
