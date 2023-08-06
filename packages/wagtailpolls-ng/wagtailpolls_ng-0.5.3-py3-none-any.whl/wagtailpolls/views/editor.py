import logging
import pprint

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.lru_cache import lru_cache
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import ObjectList, extract_panel_definitions_from_model_class

from wagtailpolls import models

logger = logging.getLogger(__name__)


@lru_cache(maxsize=256)
def get_poll_edit_handler(model) -> ObjectList:
    panels = extract_panel_definitions_from_model_class(model)
    logger.debug(f"get_poll_edit_handler({model}) panels = {pprint.pformat(panels, indent=2)}")
    edit_handler_class = ObjectList(panels).bind_to_model(model=model)
    logger.debug(f"get_poll_edit_handler({model}) edit_handler_class = {edit_handler_class}")
    return edit_handler_class


@permission_required("wagtailadmin.access_admin")  # further permissions are enforced within the view
def create(request):
    edit_handler_class = get_poll_edit_handler(model=models.Poll)
    form_class = edit_handler_class.get_form_class()
    poll = models.Poll

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            poll = form.save()
            poll.save()
            messages.success(request, _('The poll "{0!s}" has been added').format(poll))
            return redirect("wagtailpolls_index")
        else:
            messages.error(request, _("The poll could not be created due to validation errors"))
            edit_handler = edit_handler_class(form=form, instance=poll)
    else:
        form = form_class()
        edit_handler = edit_handler_class(form=form, instance=poll)

    return render(
        request,
        "wagtailpolls/create.html",
        {
            "form": form,
            "edit_handler": edit_handler,
        },
    )


@permission_required("wagtailadmin.access_admin")  # further permissions are enforced within the view
def edit(request, poll_pk):
    poll = get_object_or_404(models.Poll, pk=poll_pk)

    EditHandler = get_poll_edit_handler(models.Poll)
    EditForm = EditHandler.get_form_class()

    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=poll)

        if form.is_valid():
            poll = form.save()
            poll.save()
            messages.success(request, _('The poll "{0!s}" has been updated').format(poll))
            return redirect("wagtailpolls_index")

        else:
            messages.error(request, _("The poll could not be updated due to validation errors"))
            edit_handler = EditHandler(instance=poll, form=form)
    else:
        form = EditForm(instance=poll)
        edit_handler = EditHandler(instance=poll, form=form)

    return render(
        request,
        "wagtailpolls/edit.html",
        {
            "poll": poll,
            "form": form,
            "edit_handler": edit_handler,
        },
    )


@permission_required("wagtailadmin.access_admin")  # further permissions are enforced within the view
def delete(request, poll_pk):
    poll = get_object_or_404(models.Poll, pk=poll_pk)

    if request.method == "POST":
        poll.delete()
        return redirect("wagtailpolls_index")

    return render(
        request,
        "wagtailpolls/delete.html",
        {
            "poll": poll,
        },
    )


@permission_required("wagtailadmin.access_admin")  # further permissions are enforced within the view
def copy(request, poll_pk):
    poll = models.Poll.objects.get(id=poll_pk)

    if request.method == "POST":
        poll.pk = None
        poll.save()
        return redirect("wagtailpolls_index")

    return render(
        request,
        "wagtailpolls/copy.html",
        {
            "poll": poll,
        },
    )
