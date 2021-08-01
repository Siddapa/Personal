from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    data = request.POST
    print(data)
    return render(request, 'index.html')