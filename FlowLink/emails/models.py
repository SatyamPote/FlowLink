from django.db import models

class Email(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200)
    summary = models.TextField()
    date_received = models.DateTimeField()

    def get_summary(self):
        return self.summary[:100]  # Truncate to 100 characters for the summary
