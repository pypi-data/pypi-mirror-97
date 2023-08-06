import logging

from django.contrib.contenttypes.models import ContentType
from wagtail.admin.edit_handlers import BaseChooserPanel

from . import models
from .widgets import AdminPollChooser

logger = logging.getLogger(__name__)


class PollChooserPanel(BaseChooserPanel):
    object_type_name = "poll"
    snippet_type = None

    def widget_overrides(self):
        return {self.field_name: AdminPollChooser(content_type=ContentType.objects.get_for_model(models.Poll))}

    def __init__(self, field_name, *args, **kwargs):
        self.snippet_type = kwargs.pop("snippet_type", None)
        super().__init__(field_name=field_name, *args, **kwargs)
