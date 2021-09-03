from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def pricing(request):
    return render(request, 'pricing.html')
