from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from devicesapi.models import Dispositivo, Configuracoes, Dados, Mensagens
from accounts.models import Account, Plano
from .forms import DispositivoForm, ConfiguracaoForm
from .estatisticas import Estatisticas


@login_required(login_url='login')
def device_register(request, pk):
    user = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = DispositivoForm(request.POST or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']  # criar uma regra para o nome ser unico
            serial = form.cleaned_data['serial']
            placa = form.cleaned_data['placa']
            tipo = form.cleaned_data['tipo']
            dispositivo = Dispositivo.objects.create(usuario=user, nome=nome, serial=serial, placa=placa, tipo=tipo)
            configuracao = Configuracoes.objects.create(dispositivo=dispositivo)
            try:
                plano = Plano.objects.get(usuario=user)
            except:
                if user.devices_created == user.device_limit_creation:
                    return redirect('dashboard')
                user.devices_created += 1
                user.save()
            dispositivo.save()
            configuracao.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm()
    context = {
        'form': form
    }
    return render(request, 'devices/deviceregister.html', context)


# slug:dispositivo_serial
@login_required(login_url='login')
def device_update(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm(instance=device)
    context = {'form': form}
    return render(request, 'devices/deviceupdate.html', context)


@login_required(login_url='login')
def device_delete(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard')
    context = {'device': device}
    return render(request, 'devices/devicedelete.html', context)


@login_required(login_url='login')
def device_conf(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    configuracao = Configuracoes.objects.get(dispositivo=device)
    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, instance=configuracao)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ConfiguracaoForm(instance=configuracao)
    context = {'form': form}
    return render(request, 'devices/deviceconf.html', context)


@login_required(login_url='login')
def device_graphic(request, dispositivo_serial):   # precisa de ajustes
    device = Dispositivo.objects.get(serial=dispositivo_serial)
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
    return render(request, 'devices/device_graphic.html', context)


@login_required(login_url='login')
def device_statistics(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    dados = Dados.objects.filter(dispositivo=device)

    # limite para dados a partir do plano do usuario
    cont_data = dados.count()
    flag_data_limit = False
    try:
        plano = Plano.objects.get(usuario=device.usuario)
        print(plano)
        #  lógica para usuarios pagos
    except:
        if cont_data == 20:
            flag_data_limit = True

    est = Estatisticas(dados)
    estatisticas = {
        'media': est.media(),
        'mediana': est.mediana(),
        'moda': est.moda(),
        'error': est.flag_error,
    }
    context = {'device': device, 'dados': dados, 'estatisticas': estatisticas,
               'flag_data_limit': flag_data_limit}
    return render(request, 'devices/device_statistics.html', context)


@login_required(login_url='login')
def device_messages(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    flag_not_messages = False
    flag_not_critc = False
    flag_limit_msgs = False
    critcs_msgs = []
    msgs = []

    try:
        # tenta verificar se existem alertas para o dispositivo
        mensagens = Mensagens.objects.filter(dispositivo=device)

        # verifica o limite de alertas
        cont_msgs = mensagens.count()
        try:
            plano = Plano.objects.get(usuario=mensagens.dispositivo.usuario)
            print(plano)
        except:
            if cont_msgs == 10:
                flag_limit_msgs = True

        # se o dispositivo possuir alertas:
        if len(mensagens) > 0:
            for i in mensagens:
                if i.is_critic is True:
                    critcs_msgs.append(i)
                else:
                    msgs.append(i)
        else:
            flag_not_critc = True
            flag_not_messages = True
    except:
        flag_not_messages = True
    if len(critcs_msgs) == 0:
        flag_not_critc = True

    context = {
                'device': device,
                'mensagens': msgs,
                'criticas': critcs_msgs,
                'flag_not_messages': flag_not_messages,
                'flag_not_critc': flag_not_critc,
                'flag_limit_msgs': flag_limit_msgs
    }
    return render(request, 'devices/device_messages.html', context)
