"""Base classes for transactional emails"""
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import mail_admins
from django.core.mail import send_mail
from django.db.utils import ProgrammingError
from html2text import HTML2Text
from render_block import BlockNotFound, render_block_to_string
from xml.etree import ElementTree

from .models import SentMail

class Email:
    template = None
    from_email = settings.DEFAULT_FROM_EMAIL
    user = None

    def __init__(self, ctx, to_email):
        if self.template is None:
            raise ProgrammingError("Email subclasses must set template")

        self.to_email = to_email

        ctx = {'BASE_URL': settings.BASE_URL, **ctx}
        self.ctx = ctx

        self.subject = render_block_to_string(self.template, 'subject', ctx).strip()

        # Make links absolute
        self.html = render_block_to_string(self.template, 'html', ctx)
        self._make_links_absolute()

        try:
            self.plain = render_block_to_string(self.template, 'plain', ctx).strip()
        except BlockNotFound:
            h = HTML2Text()
            h.ignore_images = True
            h.ignore_emphasis = True
            h.ignore_tables = True
            self.plain = h.handle(self.html)

    def send(self):
        send_mail(
            self.subject,
            self.plain,
            self.from_email,
            [self.to_email],
            html_message=self.html
        )

        log = SentMail(
            class_name=self.__class__.__name__,
            email_address=self.to_email,
            subject=self.subject,
            plain_body=self.plain,
            html_body=self.html
        )
        if self.user:
            log.user = self.user
        log.save()

        self.after_send(log=log) # pylint: disable=no-member

    def after_send(self, *args, **kwargs):
        """Called after an email is sent"""

    @classmethod
    def get_for_preview(cls, request):
        return cls({}, 'nobody@example.com')

    def _make_links_absolute(self):
        """Make all src and href attrs in the html document absolute"""
        root = ElementTree.fromstring(self.html)

        for att in ('src', 'href'):
            for tag in root.findall(f'.//*[@{att}]'):
                tag.attrib[att] = urljoin(settings.BASE_URL, tag.attrib[att])

        self.html = ElementTree.tostring(root, method="html", encoding="unicode")

class UserEmail(Email):
    def __init__(self, ctx, user):
        self.user = user
        ctx = {'user': user, **ctx}

        super().__init__(ctx, user.email)


class AdminEmail(Email):
    def __init__(self, ctx):
        super().__init__(ctx, None)

    def send(self):
        mail_admins(
            self.subject,
            self.plain,
            html_message=self.html
        )
