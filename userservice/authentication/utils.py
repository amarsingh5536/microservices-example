import re

EMAIL_REGEX = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.([a-zA-Z]{3,5}|[a-zA-Z]{2,5}\.[a-zA-Z]{2,5})'
)
