from django.core.exceptions import ValidationError

def validate_receipt_file(file):
    max_size = 2 * 1024 * 1024

    valid_types = [
        'application/pdf',
        'image/png',
        'image/jpeg',
    ]

    if file.size > max_size:
        raise ValidationError("Receipt file size must be 2MB or less.")

    if file.content_type not in valid_types:
        raise ValidationError("Only PDF, PNG, and JPG files are allowed.")