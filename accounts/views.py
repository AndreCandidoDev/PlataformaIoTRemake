from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from devicesapi.models import Dispositivo, Dados, Configuracoes
from .forms import AccountForm, DispositivoForm, ConfiguracaoForm
from .models import Account
from rest_framework.authtoken.models import Token


# ===========================================Create, Update and Delete device=================================
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
            configuracao = Configuracoes.objects.create(dispositivo=dispositivo)
            dispositivo.save()
            configuracao.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/deviceregister.html', context)


# bug, ao atualizar esta criando dispositivo  --> resolvido removendo o action do form html
@login_required(login_url='login')
def device_update(request, pk):
    device = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm(instance=device)
    context = {'form': form, 'atualizar': True}
    return render(request, 'accounts/deviceupdate.html', context)


@login_required(login_url='login')
def device_delete(request, pk):
    device = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard')
    context = {'device': device}
    return render(request, 'accounts/devicedelete.html', context)


# =============================================================================================================

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


# =============================================================================================================
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    devices = Dispositivo.objects.filter(usuario=user)
    leituras = []
    confs = []
    for i in devices:
        dados = Dados.objects.filter(dispositivo=i)
        try:
            configuracoes = Configuracoes.objects.get(dispositivo=i)
            confs.append(configuracoes)
        except:
            pass
        ultimo = dados.last()
        leituras.append(ultimo)
    contagem = devices.count()
    print(confs)
    context = {'devices': devices, 'counter': contagem, 'ultimas_leituras': leituras, 'confs': confs}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def device_conf(request, pk):
    configuracao = get_object_or_404(Configuracoes, pk=pk)
    print(configuracao)
    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, instance=configuracao)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ConfiguracaoForm(instance=configuracao)
    context = {'form': form}
    return render(request, 'accounts/deviceconf.html', context)


@login_required(login_url='login')
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


# ==============================================================================================================
import statistics


class Estatisticas:
    def __init__(self, dados):
        self.dados = dados
        self.dates = dados
        self.flag_error = False

    def conv_data_to_string(self):
        aux = []
        for i in self.dados:
            aux.append(float(i.dado))
        return aux

    def conv_datetime_to_string(self):
        aux = []
        for i in self.dates:
            datas = str(i.criacao)
            conv = datas.split(' ')
            hora_format = conv[1].split('.')[0]
            aux.append(f'{conv[0]}-{hora_format}')
        return aux

    def error(self):
        dates = self.conv_datetime_to_string()
        print(dates)
        self.flag_error = True
        return dates

    def media(self):
        try:  # calcula para dados numericos
            self.dados = self.conv_data_to_string()
            return statistics.mean(self.dados)
        except:  # mostra quantas leituras foram obtidas
            return self.error()

    def mediana(self):
        if self.flag_error:
            pass
        else:
            return statistics.median(self.dados)

    def moda(self):
        if self.flag_error:
            pass
        else:
            return statistics.mode(self.dados)


@login_required(login_url='login')
def device_statistics(request, pk):
    device = Dispositivo.objects.get(id=pk)
    dados = Dados.objects.filter(dispositivo=device)
    est = Estatisticas(dados)
    estatisticas = {
        'media': est.media(),
        'mediana': est.mediana(),
        'moda': est.moda(),
        'error': est.flag_error
    }
    context = {'device': device, 'dados': dados, 'estatisticas': estatisticas}
    return render(request, 'accounts/device_statistics.html', context)

# ==============================================================================================================
