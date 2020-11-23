import json
import logging

from apps.api.models import UnknownWord
from apps.api.modules.markov import MarkovModel
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger("crescent")


class JsonResponseUTF8(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)


@ensure_csrf_cookie
def index(request):
    return JsonResponse({"message": "Hello World!"})


@require_POST
@csrf_exempt
def learn(request):
    data = json.loads(request.body)
    logger.debug("learning: " + data["input_text"])
    markov = MarkovModel()
    descriptions = markov.learn(data["input_text"])
    return JsonResponseUTF8(
        {
            "input_text": data["input_text"],
            "descriptions": descriptions,
        }
    )


@require_POST
@csrf_exempt
def generate(request):
    data = json.loads(request.body)
    markov = MarkovModel()
    input_text = data["input_text"] if "input_text" in data else None
    options = data["options"] if "options" in data else []
    output_text, descriptions = markov.generate(input_text, options)
    return JsonResponseUTF8(
        {
            "input_text": input_text,
            "output_text": output_text,
            "descriptions": descriptions,
        }
    )


@require_POST
@csrf_exempt
def pop_unknown_words(request):
    data = json.loads(request.body)
    unknown_words = UnknownWord.objects.all()
    if "limit" in data:
        unknown_words = unknown_words[: data["limit"]]
    result = {
        "unknown_words": [
            {"id": unk.word.id, "name": unk.word.name} for unk in unknown_words
        ]
    }
    UnknownWord.objects.filter(word_id__in=[unk.id for unk in unknown_words]).delete()
    return JsonResponseUTF8(result)
