"""Template tags to make e-mail styling less painful"""
import cssutils
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()


_styles = None


@register.simple_tag()
def style(names):
    global _styles
    if _styles is None or settings.DEBUG:
        _load_styles()

    css = ';'.join(_styles.get(name, '') for name in names.split())
    return mark_safe('style="%s"' % css)


def _load_styles():
    global _styles
    _styles = {}

    if settings.EMAIL_STYLESHEET:
        fname = finders.find(settings.EMAIL_STYLESHEET)
        if not fname:
            raise ImproperlyConfigured("Couldn't find stylesheet %s" % settings.EMAIL_STYLESHEET)

        sheet = cssutils.parseFile(fname)
        for rule in sheet.cssRules:
            for selector in rule.selectorList:
                _styles[selector.selectorText] = rule.style.cssText
