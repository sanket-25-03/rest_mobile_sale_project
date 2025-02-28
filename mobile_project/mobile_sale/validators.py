from django.core.exceptions import ValidationError

def validate_imei_number(value):
    if not value.isdigit() or len(value) != 15:
        raise ValidationError("IMEI number must be a 15-digit numeric string.")
    return value