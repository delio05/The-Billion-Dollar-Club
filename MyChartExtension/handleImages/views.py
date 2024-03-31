import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

debug = True
load_dotenv()
totalFeedback = 0
positiveFeedback = 0

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")

BACKRGOUND_PROMPT = "You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will directly give your explanation with middle school level semantics in {}."
REVIEWING_PROMPT = "You are a doctor. Your coworker just gave a summarization to a piece of text given by a user. Please check if they miss any important information. Your coworker's summarization is '{}'. You will directly give your short explanation to the patient with necessary changes in middle school level semantics in {}."


def get_feedback(request):
    userInput = str(request.GET.get('attitude'))
    totalFeedback += 1
    if userInput == 'positive':
        positiveFeedback += 1
    if debug: 
        print("Current totalFeedback: " + totalFeedback + " with positive feedback rate: " + 100*(positiveFeedback/totalFeedback))

def get_sentence(request):
    userInput = request.GET.get('content')
    language = request.GET.get('language', default = "English")
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
                    "content": BACKRGOUND_PROMPT.format(language),
                },
                {
                    "role":"user",
                    "content": userInput,
                }
            ]
        )
        response = _response.choices[0].message.content
        _response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = [
                {
                    "role":"system",
                    "content": REVIEWING_PROMPT.format(response, language),
                },
                {
                    "role":"user",
                    "content": userInput,
                }
            ]
        )
        response = _response.choices[0].message.content

        returnData = {
            'result': "Successful",
            'language': language,
            'content': response,
        }
        if debug:
            print(returnData)
        return JsonResponse(returnData)
    except openai.APIConnectionError as e:
        messages.warning(request, f"Failed to connect to OpenAI API...")
    except openai.RateLimitError as e:
        messages.warning(request, f"Exceed current quota...")
    except Exception as e:
        messages.warning(e.__context__)