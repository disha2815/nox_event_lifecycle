from django import forms
from .models import Participant, Event, Registration
from .validators import validate_receipt_file

class RegistrationForm(forms.ModelForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        empty_label="Select an event"
    )

    class Meta:
        model = Participant
        fields = [
            'student_id',
            'name',
            'email',
            'transaction_id',
            'receipt',
            'event',
        ]

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            validate_receipt_file(receipt)
        return receipt

    def save(self, commit=True):
        event = self.cleaned_data.pop('event')
        participant = super().save(commit=commit)

        if commit:
            Registration.objects.create(
                participant=participant,
                event=event
            )

        return participant

class FeedbackForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            validate_receipt_file(receipt)
        return receipt


class FeedbackForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea, required=False)