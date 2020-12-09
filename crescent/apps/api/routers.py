from apps.api.models import UnknownWord
from apps.api.modules.markov import MarkovModel
from apps.api.schemas import Context, Contexts, PopUnknownWordsOption
from django.http import JsonResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index():
    return JsonResponse({"message": "Hello World!"})


@router.post("/listen")
def listen(context: Context):
    markov = MarkovModel()
    return {
        "input_text": context.input_text,
        "descriptions": markov.learn(context.input_text),
    }


@router.post("/learn")
def learn(contexts: Contexts):
    markov = MarkovModel()
    learned_data = [
        {
            "input_text": context.input_text,
            "options": context.options,
            "descriptions": markov.learn(context.input_text),
        }
        for context in contexts.contexts
    ]
    return {"learned_data": learned_data}


@router.post("/generate")
def generate(context: Context):
    markov = MarkovModel()
    output_text, descriptions = markov.generate(
        context.input_text,
        context.options,
    )
    return {
        "input_text": context.input_text,
        "options": context.options,
        "output_text": output_text,
        "descriptions": descriptions,
    }


@router.post("/unknown-words/pop")
def pop_unknown_words(option: PopUnknownWordsOption):
    unknown_words = UnknownWord.objects.all()
    if option.limit:
        unknown_words = unknown_words[: option.limit]
    result = {
        "unknown_words": [
            {"id": unk.word.id, "name": unk.word.name} for unk in unknown_words
        ]
    }
    UnknownWord.objects.filter(word_id__in=[unk.id for unk in unknown_words]).delete()
    return result
