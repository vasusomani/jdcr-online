# custom_tags.py
from django import template
import re

register = template.Library()

@register.filter(name='extract_numbers')
def extract_numbers(value):
    """
    Custom template filter to extract numbers from a string.
    """
    if value:
        # Use regular expression to find all numeric characters in the string
        numbers = re.findall(r'\d+', value)
        if numbers:
            # Join the numeric characters and convert to an integer
            return int(''.join(numbers))
    return 0  # Default value if no numbers are found