from django.shortcuts import render
from django.http import JsonResponse
import socket
# Create your views here.

def get_hosname(request):
    data = {
        'hostname': socket.gethostname()
    }
    return JsonResponse(data)