import re

# Import SQLAlchemy ModelView.
from flask_admin.contrib.sqla import ModelView

# Import WTForms libraries.
from wtforms import ValidationError, PasswordField


def is_valid_hostname(hostname):
    """
    Validate a hostname.
    http://stackoverflow.com/questions/2532053/validate-a-hostname-string
    """
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


class FarmView(ModelView):
    """Extend the ModelView class for Farm models."""

    # Exclude the password field from columns and configure it as a password.
    column_exclude_list = ['password']
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    # Validate URLs.
    def valid_url(form, field):
        if not is_valid_hostname(field.data):
            raise ValidationError('Invalid URL.')
    form_args = {
        'url': {
            'validators': [valid_url]
        }
    }
