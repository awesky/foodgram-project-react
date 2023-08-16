from django.http import HttpResponse
# from django.shortcuts import render


# Create your views here.
def recipes_index(request):
    return HttpResponse('Testing home page of --recipies--')
