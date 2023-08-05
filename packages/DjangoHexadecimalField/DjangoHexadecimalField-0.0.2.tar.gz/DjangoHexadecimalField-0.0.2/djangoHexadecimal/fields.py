import re
import django
from django.core.validators import RegexValidator
from django.db import models
if django.VERSION >= (2, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _

HEXA_RE = re.compile('^[A-Fa-f0-9]+$')
HEXA_VALID = RegexValidator(HEXA_RE, _('Enter a valid hex number '), 'invalid')


class HexadecimalField(models.CharField):

    def __init__(self, *args, **kwargs):
        self.validators += [HEXA_VALID]

        super(HexadecimalField, self).__init__(*args, **kwargs)
