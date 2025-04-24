from django.shortcuts import render
from django.http import JsonResponse

STATE_MESSAGES = {'messages': [], 'status': False}

def get_parsing_progress(request):
    return JsonResponse(STATE_MESSAGES)

def parsing_progress_view(request):
    return render(request, 'parsing_progress.html')
