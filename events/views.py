from django.http import HttpResponse

from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>🎓 Event Lifecycle & Certification System</h1>
        <p>Project is running successfully.</p>
        <a href="/dashboard/">Go to Dashboard</a>
        <br><br>
        <a href="/admin/">Go to Django Admin</a>
    """)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Registration

def generate_certificate(request, reg_id):
    reg = Registration.objects.get(id=reg_id)

    if not reg.is_certificate_eligible():
        return HttpResponse("Certificate locked. Attendance and feedback are required.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(150, 750, "Certificate of Participation")

    p.setFont("Helvetica", 16)
    p.drawString(120, 680, f"This is awarded to {reg.participant.name}")
    p.drawString(120, 640, f"For successfully attending {reg.event.title}")
    p.drawString(120, 600, "Department of CSE, SJBIT")

    p.save()
    return response

from django.shortcuts import render

def dashboard(request):
    registrations = Registration.objects.all()
    return render(request, 'events/dashboard.html', {
        'registrations': registrations
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Registration

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})