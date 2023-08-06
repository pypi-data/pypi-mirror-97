from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from psu_infotext.models import Infotext
from psu_base.classes.Log import Log
from psu_base.services import utility_service, error_service
from psu_base.decorators import require_authority
log = Log()

# ToDo: Error Handling/Messages


@require_authority(['admin', 'infotext', 'developer'])
def infotext_index(request):
    """
    Search page for locating infotext to be edited
    """
    log.trace()

    text_instances = Infotext.objects.filter(app_code=utility_service.get_app_code())
    log.end('infotext/index')
    return render(
        request, 'infotext_index.html',
        {'text_instances': text_instances}
    )


@require_authority(['admin', 'infotext', 'developer'])
def infotext_update(request):
    """
    Update a given infotext instance
    """
    text_id = request.POST.get('id')
    text_content = request.POST.get('content')
    log.trace([text_id])

    text_instance = get_object_or_404(Infotext, pk=text_id)
    try:
        text_instance.set_content(text_content)
        text_instance.save()
        return HttpResponse(text_instance.content)
    except Exception as ee:
        error_service.unexpected_error("Unable to save infotext", ee)
        return HttpResponseForbidden()
