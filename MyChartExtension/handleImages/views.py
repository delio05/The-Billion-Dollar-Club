import os
import sys
import json

import csv

import openai
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages


load_dotenv()
debug = bool(os.environ.get("debug"))

OPENAI_client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

genai.configure(
    api_key = os.environ.get("GOOGLE_API_KEY"),
)
GOOGLE_client = genai.GenerativeModel('gemini-pro')


DATA_DIR = "/Users/halin/University of Wisconsin-Madison/2023-2024/Spring/Comp Sci 639 Capstone/The-Billion-Dollar-Club/data/feedback-{}.csv"

BACKRGOUND_PROMPT = "You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will directly give your explanation with middle school level semantics in {}. Remember, you need to make this short."
REVIEW_PROMPT = "You are a doctor. Your coworker just gave a summarization to a piece of text given by a user. Please check if they miss any important information. The original text is '{}', and your coworker's summarization is '{}'. Revise it if necessary. You will directly give your summarization in {}. Remember, you need to make this short. "
FEEDBACK_PROMPT = "You are a doctor. Your coworker just gave a summarization to a piece of text given by a user. Please check if they miss any important information. Your coworker's summarization is '{}'. Here is user's feedback: {}. You will directly give your short explanation to the patient with necessary changes in middle school level semantics in {}. Remeber, you need to make this short unless user specified other requirements."

def collect_feedback(attitude, userFeedback):
    pid = os.getpid()
    FILE_DIR = DATA_DIR.format(pid)
    fields = [attitude, userFeedback]
    with open(FILE_DIR, "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def get_feedback(request):
    userInput = request.GET.get('content')
    language = request.GET.get('language', default = "English")
    previousResponse = request.GET.get('previous')
    attitude = request.GET.get('attitude')
    userFeedback = request.GET.get('feedback')
    collect_feedback(attitude, userFeedback)
    if attitude == 'negative':
        try:
            if debug:
                print("loading...")
            if debug: print("start to acquire response...")
            _response = OPENAI_client.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = [
                    {
                        "role":"system",
                        "content": FEEDBACK_PROMPT.format(previousResponse, userFeedback, language),
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
    else:
        returnData = {
            'result' : "Successful",
            'language': language,
            'content': "Feedback collected",
        }
        return JsonResponse(returnData)


def get_sentence(request):
    userInput = request.GET.get('content')
    language = request.GET.get('language', default = "English")
    userInput = str(userInput).strip()
    if debug:
        print("userInput: ", userInput)
    try:
        if debug: print("start to acquire response...")
        _response = OPENAI_client.chat.completions.create(
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
        response = GOOGLE_client.generate_content(REVIEW_PROMPT.format(userInput, response, language)).text
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

def index(request):
    return HttpResponse("Hello, World! You are about to pass an image.")