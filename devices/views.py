from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from devicesapi.models import Dispositivo, Configuracoes, Dados, Mensagens, Acoes
from accounts.models import Account, Plano
from .forms import DispositivoForm, ConfiguracaoForm, AcaoForm
from .estatisticas import Estatisticas
import hashlib
import csv

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def cria_serial(nome, placa, tipo, email):
    enc_str = nome.encode('utf-8')+placa.encode('utf-8')+tipo.encode('utf-8')+email.encode('utf-8')
    hashserial = hashlib.sha512()
    hashserial.update(enc_str)
    serial = hashserial.hexdigest()
    return serial


def create_conf(dispositivo):
    configuracao = Configuracoes.objects.create(dispositivo=dispositivo)
    configuracao.save()


def create_acao(dispositivo):
    acao = Acoes.objects.create(dispositivo=dispositivo)
    acao.save()


@login_required(login_url='login')
def device_register(request, pk):
    user = Account.objects.get(id=pk)
    devices_count_aux = Dispositivo.objects.filter(usuario=user).count()
    if request.method == 'POST':
        form = DispositivoForm(request.POST or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            placa = form.cleaned_data['placa']
            tipo = form.cleaned_data['tipo']
            print(tipo, type(tipo))
            nome = nome + str(request.user.email).split('@')[0]+str(devices_count_aux)
            serial = cria_serial(nome, placa, tipo, user.email)
            dispositivo = Dispositivo.objects.create(usuario=user, nome=nome, serial=serial, placa=placa, tipo=tipo)

            if tipo == 'Sensor':
                create_conf(dispositivo)
            elif tipo == 'Atuador':
                create_acao(dispositivo)

            try:
                plano = Plano.objects.get(usuario=user)
            except:
                if user.devices_created == user.device_limit_creation:
                    return redirect('dashboard')
                user.devices_created += 1
                user.save()
            dispositivo.save()
            return redirect('dashboard')
    else:
        form = DispositivoForm()
    context = {
        'form': form
    }
    return render(request, 'devices/deviceregister.html', context)


def device_serial(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    context = {'device': device}
    return render(request, 'devices/deviceserial.html', context)


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


def device_acao(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    acao = Acoes.objects.get(dispositivo=device)
    if request.method == 'POST':
        form = AcaoForm(request.POST, instance=acao)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AcaoForm(instance=acao)
    context = {'form': form}
    return render(request, 'devices/deviceacao.html', context)


def trata_horario_medicao(dado_medicao):
    aux = dado_medicao.split(' ')
    data = aux[0]
    aux_data = data.split('-')
    hora = aux[1].split('.')[0]
    data_formatada = f'{aux_data[2]}/{aux_data[1]}/{aux_data[0]}'
    medicao = f'{data_formatada}-{hora}'
    return medicao


@login_required(login_url='login')
def device_statistics(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    dados = Dados.objects.filter(dispositivo=device)

    horarios_medicoes = []
    leituras = []
    for i in dados:
        data = trata_horario_medicao(str(i.criacao))
        horarios_medicoes.append(data)
        try:
            leituras.append(float(i.dado))
        except:
            leituras.append(str(i.dado))

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
               'flag_data_limit': flag_data_limit, 'medicoes': horarios_medicoes, 'leituras': leituras}
    return render(request, 'devices/device_statistics.html', context)


@login_required(login_url='login')
def device_csv_generator(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    dados = Dados.objects.filter(dispositivo=device)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newcsvfile.csv"'
    writer = csv.writer(response)
    writer.writerow(['Horario', 'Leitura', 'Unidade'])
    for i in dados:
        writer.writerow([trata_horario_medicao(str(i.criacao)), i.dado, i.unidade])
    return response


@login_required(login_url='login')
def device_pdf_generator(request, dispositivo_serial):
    device = Dispositivo.objects.get(serial=dispositivo_serial)
    dados = Dados.objects.filter(dispositivo=device)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # todo: study and implement this feature
    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
            if cont_msgs == 20:
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
