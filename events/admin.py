from django.contrib import admin
from .models import Participant, Event, Registration

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'attended', 'feedback_submitted', 'certificate_status')
    list_filter = ('attended', 'feedback_submitted')

    def certificate_status(self, obj):
        return "Eligible 🎓" if obj.is_certificate_eligible() else "Not Eligible ❌"