from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from devicesapi.models import Dispositivo, Dados, Configuracoes
from .forms import AccountForm, UserProfileForm, PlanoForm
from .models import Account, UserProfile, Plano
from rest_framework.authtoken.models import Token


@login_required(login_url='login')
def profile_register(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            endereco_completo = form.cleaned_data['endereco_completo']
            cep = form.cleaned_data['cep']
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']
            perfil = UserProfile.objects.create(user=user, cpf=cpf, endereco_completo=endereco_completo,
                                                cep=cep, cidade=cidade, estado=estado)
            perfil.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm()
    context = {'form': form}
    return render(request, 'accounts/profileregister.html', context)


@login_required(login_url='login')
def profile_update(request, pk):
    profile = UserProfile.objects.get(user=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    context = {'form': form}
    return render(request, 'accounts/profileupdate.html', context)


@login_required(login_url='login')
def plano_change(request, pk):
    user = Account.objects.get(id=pk)
    usuario = UserProfile.objects.get(user=user)
    limite_redes_iot = None
    limite_dispositivos_iot = None
    if request.method == 'POST':
        form = PlanoForm(request.POST)
        if form.is_valid():
            plano = form.cleaned_data['plano']
            periodo = form.cleaned_data['periodo']
            if plano == 'Pessoal':
                limite_redes_iot = 3
                limite_dispositivos_iot = 30
            elif plano == 'Empresarial':
                limite_redes_iot = 15
                limite_dispositivos_iot = 150
            userPlan = Plano.objects.create(usuario=user, perfil=usuario, plano=plano,
                                            limite_redes_iot=limite_redes_iot,
                                            limite_dispositivos_iot=limite_dispositivos_iot,
                                            periodo=periodo)
            userPlan.save()
            return redirect('dashboard')  # redirect to payment --> (need implementation)
    else:
        form = PlanoForm()
    context = {'form': form}
    return render(request, 'accounts/planochange.html', context)


@login_required(login_url='login')
def plano_update(request, pk):
    plano = Plano.objects.get(usuario=pk)
    if request.method == 'POST':
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlanoForm(instance=plano)
    context = {'form': form}
    return render(request, 'accounts/planoupdate.html', context)


@login_required(login_url='login')
def plano_cancel(request, pk):
    plano = Plano.objects.get(usuario=pk)
    if request.method == 'POST':
        plano.delete()
        return redirect('dashboard')
    context = {'plano': plano}
    return render(request, 'accounts/planodelete.html', context)


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
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = last_name+str(email).split('@')[0]
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
    else:
        return render(request, 'accounts/signin.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
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
        return redirect('login')
    else:
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
            return redirect('login')
        else:
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
        return redirect('resetpassword')
    else:
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
            return redirect('login')
        else:
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')


def data_to_chart(devices, usuario, tipo):
    devices_names = []
    counter = []
    padrao_background = 'rgba(54, 162, 235, 0.2)'
    padrao_borders = 'rgba(54, 162, 235, 1)'
    warning_background = 'rgba(255, 99, 132, 0.2)'
    warning_border = 'rgba(255, 99, 132, 1)'
    devices_background_colors = []
    devices_border_colors = []
    limit_datas = None
    limit_messages = None
    try:
        plano = Plano.objects.get(usuario=usuario)
    #     logica para usuario com plano
    except:
        limit_datas = 20
        limit_messages = 20
    for i in devices:
        devices_names.append(i.nome)
        if tipo == 'messages':
            cont = i.mensagens.count()
            counter.append(cont)
            if cont == limit_messages and limit_messages is not None:
                devices_background_colors.append(warning_background)
                devices_border_colors.append(warning_border)
            else:
                devices_background_colors.append(padrao_background)
                devices_border_colors.append(padrao_borders)
        elif tipo == 'dados':
            cont = i.dados.count()
            counter.append(cont)
            if cont == limit_datas and limit_datas is not None:
                devices_background_colors.append(warning_background)
                devices_border_colors.append(warning_border)
            else:
                devices_background_colors.append(padrao_background)
                devices_border_colors.append(padrao_borders)
    return devices_names, counter, devices_background_colors, devices_border_colors


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    devices_created = None
    devices_creation_limited = False
    flag_stop_device_creation = False
    limit = None  # limite de dispositivos
    flag_limit = False  # flag limite de dispositivos
    plano_type = None
    flag_has_plan = False
    network_limit = None
    flag_no_data = False
    flag_no_device = False

    try:  # informações do painel minha conta/ criar variaveis para alterar dashboard
        plano = Plano.objects.get(usuario=user)
        limit = plano.limite_dispositivos_iot
        network_limit = plano.limite_redes_iot
        plano_type = plano.plano
        flag_has_plan = True
    except:
        limit = 5
        network_limit = 'Unica'
        plano_type = 'Gratuito'
        devices_creation_limited = True
        devices_created = user.devices_created
        if devices_created == user.device_limit_creation:
            flag_stop_device_creation = True

    devices = Dispositivo.objects.filter(usuario=user)
    chart_data = data_to_chart(devices, user, 'dados')
    chart_device_names = chart_data[0]
    chart_device_data_counts = chart_data[1]
    chart_data_background_color = chart_data[2]
    chart_data_border_color = chart_data[3]

    chart_messages = data_to_chart(devices, user, 'messages')
    chart_device_message_count = chart_messages[1]
    chart_messages_background_color = chart_messages[2]
    chart_messages_border_color = chart_messages[3]

    # se usuario nao possuir dispositivos aciona a flag
    if len(devices) == 0:
        flag_no_device = True

    contagem_dispositivos = devices.count()

    if contagem_dispositivos == limit:
        flag_limit = True
    flag_has_profile = True
    try:  # check if current user has profile
        profile = UserProfile.objects.get(user=user)
        flag_has_profile = True
    except:
        flag_has_profile = False

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
        if ultimo is None:
            pass
        else:
            leituras.append(ultimo)
        if len(leituras) == 0:
            flag_no_data = True

    contagem = devices.count()

    context = {
               'devices': devices,
               'counter': contagem,
               'ultimas_leituras': leituras,
               'confs': confs,
               'flag_has_profile': flag_has_profile,
               'flag_limit': flag_limit,
               'contagem_dispositivos': contagem_dispositivos,
               'plano_type': plano_type,
               'limite_dispositivos': limit,
               'flag_has_plan': flag_has_plan,
               'network_limit': network_limit,
               'flag_no_device': flag_no_device,
               'flag_no_data': flag_no_data,
               'devices_creation_limited': devices_creation_limited,
               'devices_created': devices_created,
               'flag_stop_device_creation': flag_stop_device_creation,

               # variaveis do grafico
               'chart_device_names': chart_device_names,
               'chart_device_data_counts': chart_device_data_counts,
               'chart_data_background_color': chart_data_background_color,
               'chart_data_border_color': chart_data_border_color,
               'chart_device_message_count': chart_device_message_count,
               'chart_messages_background_color': chart_messages_background_color,
               'chart_messages_border_color': chart_messages_border_color,
    }
    return render(request, 'accounts/dashboard.html', context)
