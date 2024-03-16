import os
import json
import openai
from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")

def get_sentence(request):
    userInput = request.GET.get('content', None)
    userInput = str(userInput).strip()
    try:
        _response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role":"system",
                    "content":"You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will help patients "
                },
                {
                    "role":"user",
                    "content": "Explain the following docter note by a brief summary(directly give your explanation): " + userInput,
                }
            ]
        )
        response = _response.choices[0].message.content

        returnData = {
            'result': "Successful",
            'content': response,
        }
        return JsonResponse(returnData)
    except openai.APIConnectionError as e:
        messages.warning(request, f"Failed to connect to OpenAI API...")
    except openai.RateLimitError as e:
        messages.warning(request, f"Exceed current quota...")