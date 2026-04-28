from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Participant, Event, Registration


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_url', 'poster_preview', 'qr_preview')
    readonly_fields = ('poster_preview', 'qr_preview', 'qr_code')

    fields = (
        'title',
        'date',
        'description',
        'event_url',
        'poster',
        'poster_preview',
        'qr_code',
        'qr_preview',
    )

    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="120" />', obj.poster.url)
        return "No poster uploaded"

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="120" />', obj.qr_code.url)
        return "QR will be generated after saving"

    poster_preview.short_description = "Event Poster"
    qr_preview.short_description = "Auto QR Code"


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'participant',
        'event',
        'attended',
        'feedback_submitted',
        'certificate_link'
    )

    def certificate_link(self, obj):
        if obj.is_certificate_eligible():
            url = reverse('certificate', args=[obj.id])
            return format_html(
                '<a href="{}" target="_blank">Download 🎓</a>',
                url
            )
        return "Locked ❌"

    certificate_link.short_description = "Certificate"