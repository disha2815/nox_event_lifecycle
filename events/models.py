from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    transaction_verified = models.BooleanField(default=False)
    student_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(default="No description provided")
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    event_url = models.URLField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='event_qr/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Decide URL
        url = self.event_url if self.event_url else f"http://127.0.0.1:8000/event/{self.id}/"

        # Generate QR
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        filename = f'event_{self.id}.png'

        # Replace old QR (important for updates)
        self.qr_code.delete(save=False)
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(update_fields=['qr_code'])

class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    feedback_submitted = models.BooleanField(default=False)
    feedback_rating = models.IntegerField(blank=True, null=True)
    feedback_comment = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr/', blank=True, null=True)

    def __str__(self):
        return f"{self.participant} - {self.event}"

    def is_certificate_eligible(self):
        return (
            self.attended and
            self.feedback_submitted and
            self.participant.transaction_verified
        )
    
    