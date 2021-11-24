# Fará a ligação entre o hardware e o controller
# path example: http://192.168.0.16:8080/gpio2off

from networkscanner import NetworkScanner
import requests
import time
import sys


class Requester(object):

    # need refactor
    def __init__(self, test_mode=False):
        if test_mode is True:
            self.baseurl = 'http://192.168.0.16:8080'  # mudar conforme configurado na placa
        else:
            self.placa_qtd = 1
            self.placa = ''
            self.ip_base = ''
            if self.placa_qtd == 1:
                self.multiple_boards_flag = False
                self.baseurl = ''

    # procurar alguma forma de intanciar multiplas bases url

    def get_redeIP(self):
        if self.ip_base != '':
            rede_byte = '0'
            end_rede = self.ip_base.split('.')[0]+'.'+self.ip_base.split('.')[1]+'.'+self.ip_base.split('.')[2]+'.'+rede_byte
            return end_rede
        else:
            sys.exit()

    def get_ip(self):
        ip_inicial = self.get_redeIP()  # o usuário precisará passar o ip
        ip_final = '255'  # 255 para fazer broadcast na rede
        scan = NetworkScanner()
        scan.scannear_rede(ip_inicial, ip_final)
        while len(scan.threads) > 0:
            time.sleep(0.5)
        scan.ips_online.sort()
        for pc in scan.ips_online:
            print("PC ONLINE >> IP=%s - MAC=%s" % (pc[0], pc[1]))
        print(scan.ips)
        print("\nExistem %s dispositivos online neste momento\n\n" % len(scan.ips_online))
        if self.placa_qtd == 1:
            for i in range(0, len(scan.ips)):
                auxip = scan.ips[i]
                urlbase = 'http://'+auxip+':8080'
                param = '/test'
                url = urlbase+param
                try:
                    req = requests.get(url)
                    if req.status_code == 200:
                        param_board = '/board'
                        url_board = urlbase + param_board
                        check_board = requests.get(url_board)
                        if self.placa == check_board.text:
                            self.baseurl = urlbase
                            print(self.baseurl)
                            return self.baseurl
                except:
                    print('connection refused')

    # adicionar no codigo da nodemcu funções para todos pinos digitais
    def gpio_get(self, n, state):  # n -- numero do gpio; state --- on e off
        if self.baseurl == '':
            api_url = self.get_ip()
        try:
            url = self.baseurl + '/gpio' + str(n) + str(state)
            # print(url)
            request = requests.get(url)
            output = str(request.text)
            return self.parse_output(output)
        except OSError:
            print("Connection error, check your board and network and restart the system\n")
            print("Request our support if this error continue")
            sys.exit()

    @staticmethod
    def parse_output(output):
        saida = output.split('{')[1]
        saida = saida.split('}')[0]
        saida = saida.split(':')[2]
        return str(saida)

    @staticmethod
    def parse_analogic_output(output):
        saida = output.split('{')[1]
        saida = saida.split('}')[0]
        saida = saida.split(':')[1]
        return float(saida)

    # sensores disponiveis: termistor, dht22 (umidade e temperatura), luminosidade
    def analogic_get(self, sensor):
        if self.baseurl == '':
            self.get_ip()
        try:
            url = self.baseurl + '/analogic/'
            if sensor == 'termistor':
                url = url + 'termistor'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'luminosity':
                url = url + 'luminosity'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'dht11/temperature':
                url = url + 'dht11/temperature'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'dht22/temperature':
                url = url + 'dht22/temperature'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'dht11/umidity':
                url = url + 'dht11/umidity'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'dht22/umidity':
                url = url + 'dht22/umidity'
                request = requests.get(url)
                output = str(request.text)
            elif sensor == 'mq135/co2concentration':
                url = url + 'mq135/co2concentration'
                request = requests.get(url)
                output = str(request.text)
            return self.parse_analogic_output(output)
        except OSError:
            print("Connection error, check your board and network and restart the system\n")
            print("Request our support if this error continue")
            sys.exit()
