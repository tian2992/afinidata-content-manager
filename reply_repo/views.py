from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reply_repo import models
import json

@csrf_exempt
def index(request):
    def _prepare_message(message):
        message = message[0]
        extra_items = None
        try:
            extra_items = json.loads(message.extra_items)
        except:
            extra_items = {}
        r2 = dict(text=message.content)
        r2.update(extra_items)
        result = dict(messages=[r2])
        return result
    '''{
     "messages": [
       {"text": "Welcome to the Example!"},
       {"text": "What are you up to?",
       "quick_replies": [
        {
          "title":"Loved it!",
          "block_names": ["Block 1", "Block 2"]
        },
        {
          "title":"Not really...",
          "url": "https://google.com",
          "type":"json_plugin_url"
        },
     ]
    }'''
    data = json.loads(request.body)
    if not data['locale']:
        raise Http404
    if not data['block_id']:
        raise Http404
    d = data['locale'].split('_')
    if len(d) != 2:
        raise Http404
    language = d[0]
    region = d[1]
    #First try with locale
    message = models.Message.objects.filter(
            block_id = data['block_id'],
            language = language, #  = data['locale'],
            state = 'Published'
        )
    message = list(message)
    #Else try with language
    if len(message) > 0:
        result = _prepare_message(message)
        return JsonResponse(result)
    if not message:
        message = models.Message.objects.filter(
                block_id = data['block_id'],
                language = language,
                state = 'Published'
            )
    message = list(message)
    #Else default to english
    if len(message) > 0:
        result = _prepare_message(message)
        return JsonResponse(result)
    if not message:
        message = models.Message.objects.filter(
                block_id = data['block_id'],
                language = 'en',
                state = 'Published'
            )
    message = list(message)
    if len(message) > 0:
        result = _prepare_message(message)
        return JsonResponse(result)
    if not message:
        message = 'Error - No block found in english for block_id %s and locale %s.' % (data['block_id'],
        data['locale'])
    return JsonResponse(dict(messages=[dict(text=message)]))

def translate(request):
    return HttpResponse(
    '''
    <form action="do_translate" method="post">
        <label for="language_origin">
            Language Origin
            <input type="text" name="language_origin" />
        </label>
        <label for="language_destination">
            Language Destination
            <input type="text" name="language_destination" />
        </label>
        <label for="destination_locale">
            Destination Locale
            <input type="text" name="destination_locale" />
        </label>
        <button type="submit" formaction="do">Start</button>
    </form>
    ''')

@csrf_exempt
def do_translate(request):
    from scripts.auto_translate import translate_reply_repo

    return JsonResponse(translate_reply_repo(language_origin = request.POST.get("language_origin"),
                                             language_destination = request.POST.get("language_destination"),
                                             destination_locale = request.POST.get("destination_locale")))

def fix_messages_view(request):
    return HttpResponse("""<form action="download" method="post">
    <input type="text" name="url" />

    <button type="submit" formaction="download">Download</button>
    <button type="submit" formaction="upload">Upload</button>
</form>""")


@csrf_exempt
def download_messages(request):
    mess_ur = request.POST.get("url")
    from scripts.reply_export_import import run_dump
    return JsonResponse(repr(run_dump(mess_ur)))


@csrf_exempt
def upload_messages(request):
    sheet_url = request.POST.get("url")
    from scripts.reply_export_import import run_up
    return JsonResponse(run_up(sheet_url))
