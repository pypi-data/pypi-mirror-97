from bs4 import BeautifulSoup
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.http.response import HttpResponse, Http404

from .models import SentMail
from . import registry
from .registry import _default_registry

@admin.register(SentMail)
class SentMailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email_address', 'user', 'timestamp')



class RegisteredEmailType(SentMail):
    class Meta:
        proxy = True


@admin.register(RegisteredEmailType)
class RegisteredEmailAdmin(admin.ModelAdmin):
    def changelist_view(self, request, **kwargs):
        response = super().changelist_view(request, **kwargs)
        response.context_data['summary'] = _default_registry._registry.keys()

        return response

    def get_urls(self):
        urls = [
            path('<slug:name>/preview/',
                self.admin_site.admin_view(self.preview),
                name="transactional_mail_preview"
            )
        ] + super().get_urls()
        return urls

    def preview(self, request, name):
        klass = registry.get_handler(name)
        if not klass:
            raise Http404()

        email = klass.get_for_preview(request)

        if request.GET.get('plain'):
            text = "Subject: %s\n\n%s" % (email.subject, email.plain)
            return HttpResponse(text, content_type="text/plain")
        else:
            # Insert an extra table with email metadata
            extra = render_to_string(
                'admin/transactional_mail/preview_table.html',
                {'email': email}
            )
            soup = BeautifulSoup(email.html, 'html.parser')
            if soup.head.title:
                title = soup.head.title
            else:
                title = soup.new_tag('title')
                soup.head.insert(0, title)
            title.string = email.subject

            soup.body.insert(0, BeautifulSoup(extra, 'html.parser'))
            return HttpResponse(soup.encode())
