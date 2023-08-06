from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.urls import include, reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from . import urls


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        url(r"^polls/", include(urls)),
    ]


@hooks.register("construct_main_menu")
def construct_main_menu(request, menu_items):
    menu_items.append(MenuItem(_("Polls"), reverse("wagtailpolls_index"), classnames="icon icon-group", order=250))
