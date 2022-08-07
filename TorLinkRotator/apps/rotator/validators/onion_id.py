from django.core import validators


class OnionV3Validator(validators.RegexValidator):
    
    regex = r"^[a-z2-7]{56}$"
