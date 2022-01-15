from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Plano
from devicesapi.models import Dispositivo, Acoes, Configuracoes, Dados, Mensagens
from devices.forms import AcaoForm, ConfiguracaoForm
from .models import Rede, DispositivoRede
from .forms import DispositivoRedeForm
import hashlib
import time

# limite de 10 dispositivos por rede (container)
# pessoal: 3 redes; empresarial: 15 redes


def cria_identificador(usuario, plano):
    todas_redes = Rede.objects.all()
    total = todas_redes.count()
    enc_str = usuario.first_name.encode('utf-8')+usuario.email.encode('utf-8')+plano.encode('utf-8')+str(time.time).encode('utf-8')
    enc_str += str(Rede.criacao).encode('utf-8')+str(total).encode('utf-8')
    hashserial = hashlib.sha512()
    hashserial.update(enc_str)
    identificador = hashserial.hexdigest()
    return identificador


def cria_serial(nome, placa, tipo, nome_rede):
    enc_str = nome.encode('utf-8')+placa.encode('utf-8')+tipo.encode('utf-8')+nome_rede.encode('utf-8')
    hashserial = hashlib.sha512()
    hashserial.update(enc_str)
    serial = hashserial.hexdigest()
    return serial


def create_conf(dispositivo_rede):
    configuracao = Configuracoes.objects.create(dispositivo_rede=dispositivo_rede)
    configuracao.save()


def create_acao(dispositivo_rede):
    acao = Acoes.objects.create(dispositivo_rede=dispositivo_rede)
    acao.save()


@login_required(login_url='login')
def network_register(request, pk):
    usuario = Account.objects.get(id=pk)
    counter = Rede.objects.filter(usuario=usuario).count()
    dispositivos_gratuitos = None
    try:
        dispositivos_gratuitos = Dispositivo.objects.filter(usuario=usuario)
    except:
        pass
    if usuario.networks_created == usuario.network_limit_creation:
        return redirect('dashboard')
    else:
        planodb = Plano.objects.get(usuario=usuario)
        plano = planodb.plano
        if request.method == 'POST':
            identificador = cria_identificador(usuario=usuario, plano=plano)
            nome = 'rede'+usuario.email.split('@')[0]+str(counter)
            rede = Rede.objects.create(usuario=usuario, plano=planodb, nome_rede=nome, identificador=identificador)
            rede.save()
            if dispositivos_gratuitos is not None:
                for dispositivo in dispositivos_gratuitos:
                    dispositivo.delete()
            usuario.networks_created += 1
            usuario.save()
            return redirect('dashboard')
    return render(request, 'networks/network_register.html')


@login_required(login_url='login')
def network_delete(request, identificador):
    usuario = Account.objects.get(email=request.user)
    rede = Rede.objects.get(identificador=identificador)
    if request.method == 'POST':
        rede.delete()
        usuario.networks_created -= 1
        usuario.save()
        return redirect('dashboard')
    return render(request, 'networks/network_delete.html')


# ==================================== Devices network ==============================================================
@login_required(login_url='login')
def device_network_register(request, identificador):
    rede = Rede.objects.get(identificador=identificador)
    nome_rede = rede.nome_rede
    if rede.qtd_dispositivos_rede == rede.limite_dispositivos_rede:
        return redirect('dashboard')
    dispositivorede_count_aux = DispositivoRede.objects.filter(rede=rede).count()
    if request.method == 'POST':
        form = DispositivoRedeForm(request.POST or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            ip = form.cleaned_data['ip']
            placa = form.cleaned_data['placa']
            tipo = form.cleaned_data['tipo']
            nome = nome + str(request.user.email).split('@')[0] + str(dispositivorede_count_aux)
            serial = cria_serial(nome, placa, tipo, rede.nome_rede)
            dispositivo_rede = DispositivoRede.objects.create(rede=rede, ip=ip, nome=nome, serial=serial,
                                                              placa=placa, tipo=tipo)
            if tipo == 'Sensor':
                create_conf(dispositivo_rede)
            elif tipo == 'Atuador':
                create_acao(dispositivo_rede)
            dispositivo_rede.save()
            rede.qtd_dispositivos_rede += 1
            rede.save()
            return redirect('dashboard')
    else:
        form = DispositivoRedeForm()
    context = {'form': form, 'nome_rede': nome_rede}
    return render(request, 'networks/device_network_register.html', context)


def device_network_update(request, dispositivo_serial):
    dispositivo_rede = DispositivoRede.objects.get(serial=dispositivo_serial)
    tipo_inicial = dispositivo_rede.tipo
    if request.method == 'POST':
        form = DispositivoRedeForm(request.POST, instance=dispositivo_rede)
        if form.is_valid():
            try:
                if tipo_inicial == form.cleaned_data['tipo']:
                    raise Exception('Tipo device igual ao anterior')

                # se o device foi atualizado para atuador
                if form.cleaned_data['tipo'] == 'Atuador':
                    create_acao(dispositivo_rede)
                    try:
                        conf = Configuracoes.objects.get(dispositivo_rede=dispositivo_rede)
                        conf.delete()
                    except:
                        pass

                # se o device foi atualizado para sensor
                elif form.cleaned_data['tipo'] == 'Sensor':
                    create_conf(dispositivo_rede)
                    try:
                        acao = Acoes.objects.get(dispositivo_rede=dispositivo_rede)
                        acao.delete()
                    except:
                        pass
            except:
                pass
            form.save()
            return redirect('dashboard')
    else:
        form = DispositivoRedeForm(instance=dispositivo_rede)
    context = {'form': form}
    return render(request, 'networks/device_network_update.html', context)


def device_network_delete(request, dispositivo_serial):
    dispositivo_rede = DispositivoRede.objects.get(serial=dispositivo_serial)
    if request.method == 'POST':
        dispositivo_rede.delete()
        return redirect('dashboard')
    context = {'device': dispositivo_rede}
    return render(request, 'networks/device_network_delete.html', context)


def device_network_configuration(request, dispositivo_serial):
    is_sensor = False
    is_atuador = False
    form = None
    dispositivo_rede = DispositivoRede.objects.get(serial=dispositivo_serial)
    if dispositivo_rede.tipo == 'Sensor':
        is_sensor = True
        configuracao = Configuracoes.objects.get(dispositivo_rede=dispositivo_rede)
        if request.method == 'POST':
            form = ConfiguracaoForm(request.POST, instance=configuracao)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = ConfiguracaoForm(instance=configuracao)
    elif dispositivo_rede.tipo == 'Atuador':
        is_atuador = True
        acao = Acoes.objects.get(dispositivo_rede=dispositivo_rede)
        if request.method == 'POST':
            form = AcaoForm(request.POST, instance=acao)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = AcaoForm(instance=acao)
    context = {'form': form, 'is_atuador': is_atuador, 'is_sensor': is_sensor}
    return render(request, 'networks/device_network_configuration.html', context)


def device_network_serial(request, dispositivo_serial):
    dispositivo_rede = DispositivoRede.objects.get(serial=dispositivo_serial)
    context = {'serial': dispositivo_rede.serial}
    return render(request, 'networks/device_network_serial.html', context)


# ========================= in progress ==============================================================================
def device_network_messages(request, dispositivo_serial):
    return


def device_network_statistics(request, dispositivo_serial):
    return


# ================================ Network Dashboard ==================================================================
@login_required(login_url='login')
def network_dashboard(request, identificador):
    counter_messages = 0
    counter_datas = 0
    rede_array = []
    rede = Rede.objects.get(identificador=identificador)
    rede_array.append(rede)
    dispositivos_rede = DispositivoRede.objects.filter(rede=rede)
    for dispositivo in dispositivos_rede:
        total_mensagens = Mensagens.objects.filter(dispositivo_rede=dispositivo).count()
        total_dados = Dados.objects.filter(dispositivo_rede=dispositivo).count()
        counter_messages += total_mensagens
        counter_datas += total_dados
    total_mensagens_dispositivos_rede = counter_messages
    total_dados_dispositivos_rede = counter_datas
    total_dispositivos_rede = dispositivos_rede.count()
    context = {
        'rede_array': rede_array,
        'dispositivos_rede': dispositivos_rede,
        'total_dispositivos_rede': total_dispositivos_rede,
        'total_mensagens_dispositivos_rede': total_mensagens_dispositivos_rede,
        'total_dados_dispositivos_rede': total_dados_dispositivos_rede
    }
    return render(request, 'networks/network_dashboard.html', context)

