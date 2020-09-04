import json

from apps.api.modules.markov import MarkovModel
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST

class JsonResponseUTF8(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)

@ensure_csrf_cookie
def index(request):
    return JsonResponse({'message': 'Hello World!'})

@require_POST
@csrf_exempt
def learn(request):
    data = json.loads(request.body)
    markov = MarkovModel()
    descriptions = markov.learn(data['input_text'])
    return JsonResponseUTF8({
        'input_text': data['input_text'],
        'descriptions': descriptions,
    })
