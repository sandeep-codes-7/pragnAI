from django.shortcuts import render
from django.conf import settings
import os
from dotenv import load_dotenv
import requests
from .models import Path, ForNewsLetter

from openai import OpenAI

load_dotenv()


def index(request):
    paths = Path.objects.all()
    if request.method != "POST":
        return render(request, "client/index.html",{"paths":paths})
    else:
        data = request.POST.get('email')
        if ForNewsLetter.objects(email=data):
            print("exists")
        else:
            ForNewsLetter(email=data).save()
        return render(request, "client/index.html")

def profile(request):
    return render(request, "client/profile.html")

def about(request):
    return render(request, "client/about.html")

def Error(request):
    return render(request, "client/Error.html")

def eval(request):
    return render(request, "client/eval.html")

def eval_view(request):
    if request.method != "POST":
        return render(request, "client/eval.html")

    question = request.POST.get("question", "").strip()
    # print(question)
    if not question:
        return render(request, "client/eval.html", {"error": "Please enter a question."})

    # get API key from env
    api_key = os.getenv('PERPLEXITY_API_KEY') 
    if not api_key:
        return render(request, "client/eval.html", {"error": "API key not configured. Set PERPLEXITY_API_KEY or OPENAI_API_KEY."})

    # messages content must be a string (not a tuple)
    messages = [
        {
            "role": "system",
            "content": "You are a professor who knows everything on the internet and you can give resources if asked."
        },
        {
            "role": "user",
            "content": question
        }
    ]
    # print(question)
    try:
       
        clt = OpenAI(api_key=api_key)  
        res = clt.chat.completions.create(model="o3-mini", messages=messages)
        print(res)

        # extract text/answer from common response shapes
        answer = None
        if isinstance(res, dict):
            choices = res.get("choices") or []
            print(choices)
            if choices:
                # support both shapes: choices[].message.content or choices[].text
                answer = choices[0].get("message", {}).get("content") or choices[0].get("text")
                print(answer)
        else:
            try:
                choices = getattr(res, "choices", None) or []
                if choices:
                    first = choices[0]
                    # SDK objects often have .message.content
                    msg = getattr(first, "message", None)
                    if msg:
                        answer = getattr(msg, "content", None)
                        print(answer)
                    if not answer:
                        answer = getattr(first, "text", None)
                        print(answer)
            except Exception:
                answer = None

        answer = answer or str(res)
        return render(request, "client/eval.html", {"res": answer, "question": question})
    except Exception as e:
        return render(request, "client/eval.html", {"error": str(e), "question": question})
    
def newsemails(request):
    pass