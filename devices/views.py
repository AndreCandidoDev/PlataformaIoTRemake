from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from devicesapi.models import Dispositivo, Configuracoes, Dados, Mensagens
from accounts.models import Account
from .forms import DispositivoForm, ConfiguracaoForm
from .estatisticas import Estatisticas


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
    return render(request, 'devices/deviceregister.html', context)


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
    return render(request, 'devices/deviceupdate.html', context)


@login_required(login_url='login')
def device_delete(request, pk):
    device = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard')
    context = {'device': device}
    return render(request, 'devices/devicedelete.html', context)


@login_required(login_url='login')
def device_conf(request, pk):
    configuracao = get_object_or_404(Configuracoes, pk=pk)
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
    return render(request, 'devices/device_graphic.html', context)


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
    return render(request, 'devices/device_statistics.html', context)


@login_required(login_url='login')
def device_messages(request, pk):
    device = Dispositivo.objects.get(id=pk)
    flag_not_messages = False
    flag_not_critc = False
    critcs_msgs = []
    msgs = []
    try:
        mensagens = Mensagens.objects.filter(dispositivo=device)
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
                'flag_not_critc': flag_not_critc
    }
    return render(request, 'devices/device_messages.html', context)
