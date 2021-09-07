from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def pricing(request):
    return render(request, 'pricing.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def usecases(request):
    return render(request, 'usecases.html')


def contact(request):
    return render(request, 'contact.html')


# improving when we have other user types
def examples(request):
    return render(request, 'examples.html')


def faq(request):
    return render(request, 'faq.html')


def support(request):
    return render(request, 'support.html')


def datapolitics(request):
    return render(request, 'datapolitics.html')
