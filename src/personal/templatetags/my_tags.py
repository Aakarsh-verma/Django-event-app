import re
from datetime import date, datetime
from decimal import Decimal

from django import template
from django.template import defaultfilters
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.timezone import is_aware, utc
from django.utils.translation import (
    gettext as _,
    gettext_lazy,
    ngettext,
    ngettext_lazy,
    npgettext_lazy,
    pgettext,
    round_away_from_one,
)

register = template.Library()


@register.filter(expects_localtime=True)
def days_until(value, arg=None):
    """
    For date values that are tomorrow, today or yesterday compared to
    present day return representing string. Otherwise, return a string
    formatted according to settings.DATE_FORMAT.
    """
    tzinfo = getattr(value, "tzinfo", None)
    try:
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today
    return _(str(delta.days))
    # if delta.days == 0:
    #    return _("today")
    # elif delta.days == 1:
    #    return _("tomorrow")
    # elif delta.days == -1:
    #    return _("yesterday")
    return defaultfilters.date(delta, arg)
