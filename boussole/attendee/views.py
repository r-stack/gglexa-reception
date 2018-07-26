import datetime
import json
import logging

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from jmespath import search

from .models import Token, User

L = logging.getLogger(__name__)


INTENT_ROUTER = {
    'StartHack':{
        'function': 'lookup_user',
        'followupEvent': 'StartHackResponse'
    },
    'CheckName_YES':{
        'function': 'check_in',
        'followupEvent': 'CheckName_YES_Response'
    }


}

class APIException(Exception):

    def __init__(self, status=500, message="Unknown Error"):
        self.status = 500
        self.message = message


def _check_token(request):
    try:
        L.info(request.META)
        token = request.META.get("HTTP_X_TOKEN")
        L.warn(token)
        user = User.objects.get(is_active=True, token__value=token)
        request.user = user
        L.warn("api user = %s", user)
    except User.DoesNotExist as exc:
        raise APIException(status=403, message='Invalid X_TOKEN header. %s' % token)


def _parse_body(request):
    body = request.body
    bodystr = body.decode('utf-8')
    data = None
    try:
        if bodystr:
            L.warn(bodystr)
            data = json.loads(bodystr)
    except:
        L.warn(body)
        raise APIException(403, "body is not JSON")
    request.data = data




def api(func):
    def check(request):
        try:
            _check_token(request)
            _parse_body(request)
            res = func(request)
            if not isinstance(res, HttpResponse):
                result_j = json.dumps(res)
                res = HttpResponse(result_j, content_type='application/json')
            return res
        except Exception as exc:
            status = 500
            message = "Unknown Error"
            if hasattr(exc, 'status'):
                status = getattr(exc, 'status')
            if hasattr(exc, 'message'):
                message = getattr(exc, 'message')
            err = {"error": message}
            err_j = json.dumps(err)
            res = HttpResponse(
                err_j, content_type='application/json', status=status)
            if status >= 500:
                L.exception("api call is faild")
            return res
    return check


@csrf_exempt
@api
def dialogflow_hook(request):
    data = request.data
    intent = search('queryResult.intent.displayName', data)

    router = INTENT_ROUTER.get(intent, {})
    funcname = router.get('function')
    func = globals().get(funcname)
    if not callable(func):
        raise APIException(404, 'no intent callback hook. intent=%s' % intent)
    request.router = router
    return func(request)


def lookup_user(request):
    data = request.data
    router = request.router
    query = search('queryResult.parameters.id', data)
    user = User.objects.filter(
        Q(receipt_no=query) | Q(username=query)
        | Q(phonetic=query)).first()

    result = {}
    result['query'] = query
    result['timestamp'] = timezone.now().isoformat()
    if user:
        userdict = {
            "username": user.username,
            "receipt_no": user.receipt_no,
            "phonetic": user.phonetic,
            "org_name": user.org_name,
            'check_in': user.check_in.isoformat() if user.check_in else None,
            "team": user.team.name if user.team else None
        }
        result.update(userdict)

    payload = {"followupEventInput": {
        "name": router.get('followupEvent'),
        "languageCode": "ja",
        "parameters": result
    }}
    return payload

def check_in(request):
    data = request.data
    router = request.router

    query = search('queryResult.parameters.id', data)
    if isinstance(query, float):
        query = int(query)
    user = User.objects.filter(
        Q(receipt_no=query) | Q(username=query)
        | Q(phonetic=query)).first()
    
    if not user:
        raise APIException(404, "no user. query=%s" % query)

    user.check_in = timezone.now()
    user.save()

    result = {
        'check_in': user.check_in.isoformat() if user.check_in else None
    }
    payload = {"followupEventInput": {
        "name": router.get('followupEvent'),
        "languageCode": "ja",
        "parameters": result
    }}
    return payload
