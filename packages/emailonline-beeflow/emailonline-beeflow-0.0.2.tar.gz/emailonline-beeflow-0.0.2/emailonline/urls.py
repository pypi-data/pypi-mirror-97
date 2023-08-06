"""copyright (c) 2021 Beeflow Ltd.

Author Rafal Przetakowski <rafal.p@beeflow.co.uk>"""
from django.urls import path

from emailonline.views import SeeEmailOnlineView

app_name = "emailonline"

urlpatterns = [path("see/<pk>", SeeEmailOnlineView.as_view(), name="see_email")]
