from django.shortcuts import render
from django.http import HttpResponse
import logging
import json

log = logging.getLogger('www')

# Create your views here.
def chatserver(request):
    resp = {}
    resp['hello'] = 'world'
    return render(request, 'chat/index.html', resp)
    # return HttpResponse(json.dumps(resp), content_type="application/json")