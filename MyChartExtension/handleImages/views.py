import os
import sys
import json

import openai
from openai import OpenAI
from dotenv import load_dotenv

from kafka import KafkaProducer

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

sys.path.append(~'/The-Billion-Dollar-Club/Workers/grpc')

from grpc.feedback_pb2 import feedback # type: ignore


load_dotenv()
debug = bool(os.environ.get("debug"))

def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")

FDBK_RESP_BROKER = 'localhost:9094'
FDBK_RESP_TOPIC = 'Feedback'


producer = KafkaProducer(
    bootstrap_servers = [FDBK_RESP_BROKER],
    acks = "all",
    retries = 10
)

def collect_feedback(attitude, userFeedback):
    proto_feedback = feedback(attitude = attitude, userFeedback = userFeedback)
    proto_value = proto_feedback.SerializeToString()
    producer.send(FDBK_RESP_TOPIC, value = proto_value)


def get_feedback(request):
    userInput = request.GET.get('content')
    language = request.GET.get('language', default = "English")
    previousResponse = request.GET.get('previous')
    attitude = request.GET.get('attitude')
    userFeedback = request.GET.get('feedback')
    collect_feedback(attitude, feedback)
    if attitude == 'negative':
        try:
            if debug: print("start to acquire response...")
            _response = client.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = [
                    {
                        "role":"system",
                        "content": REVIEWING_PROMPT.format(previousResponse, userFeedback, language),
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
    

BACKRGOUND_PROMPT = "You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will directly give your explanation with middle school level semantics in {}."
REVIEWING_PROMPT = "You are a doctor. Your coworker just gave a summarization to a piece of text given by a user. Please check if they miss any important information. Your coworker's summarization is '{}'. Here is user's feedback: {}. You will directly give your short explanation to the patient with necessary changes in middle school level semantics in {}."

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

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