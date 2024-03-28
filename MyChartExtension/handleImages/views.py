import os
import json
import openai
from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

debug = True

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key = OPENAI_API_KEY
)

# client = OpenAI()

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")

def get_sentence(request):
    userInput = request.GET.get('content', None)
    userInput = str(userInput).strip()
    if debug:
        print("userInput: ", userInput)
    try:
        if debug: print("start to acquire response...")
        _response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = [
                {
                    "role":"system",
                    "content":"You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will directly give your explanation with middle-school level semantics and relatively short paragraph."
                },
                {
                    "role":"user",
                    "content": userInput,
                }
            ]
        )
        response = _response.choices[0].message.content
        # print(response)

        returnData = {
            'result': "Successful",
            'content': response,
        }
        if debug:
            print(returnData)
        return JsonResponse(returnData)
    except openai.APIConnectionError as e:
        messages.warning(request, f"Failed to connect to OpenAI API...")
    except openai.RateLimitError as e:
        messages.warning(request, f"Exceed current quota...")