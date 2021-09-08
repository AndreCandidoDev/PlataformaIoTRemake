from django.shortcuts import render
from accounts.models import Plano


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


def examples(request):
    user = request.user
    gratuito = True
    pessoal = False
    empresarial = False
    try:
        plano = Plano.objects.get(usuario=user)
        if plano.plano == 'Pessoal':
            gratuito = False
            pessoal = True
        elif plano.plano == 'Empresarial':
            gratuito = False
            empresarial = True
    except:
        pass
    context = {'gratuito': gratuito, 'pessoal': pessoal, 'empresarial': empresarial}
    return render(request, 'examples.html', context)


def faq(request):
    return render(request, 'faq.html')


def support(request):
    return render(request, 'support.html')


def datapolitics(request):
    return render(request, 'datapolitics.html')
