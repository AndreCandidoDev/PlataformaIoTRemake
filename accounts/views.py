from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from devicesapi.models import Dispositivo, Dados
from .forms import AccountForm, DispositivoForm
from .models import Account
from rest_framework.authtoken.models import Token


@login_required(login_url='login')
def device_register(request, pk):
    user = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = DispositivoForm(request.POST or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']  # criar uma regra para o nome ser unico
            placa = form.cleaned_data['placa']
            tipo = form.cleaned_data['tipo']
            dispositivo = Dispositivo.objects.create(usuario=user, nome=nome, placa=placa, tipo=tipo)
            dispositivo.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/deviceregister.html', context)


@login_required(login_url='login')
def apidoc(request):
    return render(request, 'accounts/documentacao_api.html')


@login_required(login_url='login')
def token(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
    except:
        token = Token.objects.create(user=user)
    context = {'usuario': user.username, 'token': token}
    return render(request, 'accounts/token.html', context)


def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('login')
    else:
        form = AccountForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        auth.login(request, user)
        return redirect('dashboard')
        # return HttpResponse('ok')
    else:
        # messages.error(request, 'Invalid login credentials')
        return render(request, 'accounts/signin.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    # messages.success(request, 'You are logged out.')
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # messages.success(request, 'Congratulations your account is activate')
        return redirect('login')
    else:
        # messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Recovery password email sent to your email address')
            return redirect('login')
        else:
            # messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        # messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        # messages.error(request, 'This link has been expired')
        return redirect('login')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            # messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            # messages.error(request, 'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    devices = Dispositivo.objects.filter(usuario=user)
    leituras = []
    for i in devices:
        dados = Dados.objects.filter(dispositivo=i)
        ultimo = dados.last()
        leituras.append(ultimo)
    contagem = devices.count()
    context = {'devices': devices, 'counter': contagem, 'ultimas_leituras': leituras}
    return render(request, 'accounts/dashboard.html', context)


def device_graphic(request, pk):   # precisa de ajustes
    device = Dispositivo.objects.get(id=pk)
    dados = Dados.objects.filter(dispositivo=device)
    # print(dados)
    horarios_medicoes = []
    leituras = []
    for i in dados:
        # print(i.criacao)
        # horarios_medicoes.append(i.criacao) # necessario tratamento de dados
        horarios_medicoes.append(i.id)
        try:
            leituras.append(float(i.dado))
        except:
            leituras.append(str(i.dado))
    context = {'device': device, 'medicoes': horarios_medicoes, 'leituras': leituras}
    return render(request, 'accounts/device_graphic.html', context)


def device_statistics(request, pk):
    device = Dispositivo.objects.get(id=pk)
    return render(request, 'accounts/device_statistics.html')
