import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")

def get_sentence(request):
    content = request.GET.get('content', None)

    print('content: ', content)
    returnData = {
        'summary': "we recieved your sentence: " + content + "\n",
        'result': "Successful",
    }
    print('return Data:', json.dumps(returnData))
    return JsonResponse(returnData)