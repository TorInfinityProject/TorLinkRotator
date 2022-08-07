from django.core import validators


class RecipientValidator(validators.RegexValidator):
    
    regex = r"^[\w\d\=\+\-\.\%\s\:\/\…\_\)\(]{1,256}$"
