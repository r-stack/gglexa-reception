import datetime
import json
import logging
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from .models import Token

L = logging.getLogger(__name__)

@csrf_exempt
def index(request):

    try:
        L.info(request.META)
        token = request.META.get("HTTP_X_TOKEN")
        L.warn(token)
        Token.objects.get(value=token)
    except Token.DoesNotExist as exc:
        err = {"error": "Invalid X_TOKEN header"}
        err_j = json.dumps(err)
        res = HttpResponse(err_j, content_type='application/json', status=403)
        return res

    body = request.body
    L.warn(body)
    L.warn(type(body))
    bodystr = body.decode('utf-8')
    data = {}
    try:
        if bodystr:
            data = json.loads(bodystr)
    except:
        err = {"error": "body is not JSON"}
        err_j = json.dumps(err)
        res = HttpResponse(err_j, content_type='application/json', status=403)
        return res

    search = data.get('search')
    user = User.objects.filter(
        Q(attr__receipt_no=search) | Q(username=search)
        | Q(attr__phonetic=search)).first()



    result = {}
    result['input'] = data
    result['timestamp'] = datetime.datetime.now().isoformat()
    result['user'] = None
    if user:
        userdict = {
            "username": user.username,
            "receipt_no": user.attr.receipt_no,
            "phonetic": user.attr.phonetic,
            "org_name": user.attr.org_name,
            "team": user.attr.team.name if user.attr.team else None
        }
        result['user'] = userdict

    result_j = json.dumps(result)
    res = HttpResponse(result_j, content_type='application/json')
    return res
