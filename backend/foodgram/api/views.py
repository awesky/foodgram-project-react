from django.http import HttpResponse
# from django.shortcuts import render


# Create your views here.
def api_index(request):
    return HttpResponse('Testing home page of --api--')