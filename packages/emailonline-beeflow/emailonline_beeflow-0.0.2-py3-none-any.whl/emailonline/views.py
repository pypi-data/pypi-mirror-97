"""copyright (c) 2021 Beeflow Ltd.

Author Rafal Przetakowski <rafal.p@beeflow.co.uk>"""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from emailonline.models import EmailOnline


class SeeEmailOnlineView(View):
    def get(self, request, pk) -> HttpResponse:
        try:
            email_data = EmailOnline.objects.get(id=pk)
        except EmailOnline.DoesNotExist:
            messages.error(request, _("There is no such message ID"))

            return redirect(settings.DEFAULT_MAIN_PAGE)

        return HttpResponse(email_data.content)
