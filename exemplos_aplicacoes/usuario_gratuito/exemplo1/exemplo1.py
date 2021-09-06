# Caso de uso básico para exemplificar o uso da API em apenas 1 dispositivo
# antes de tudo voce precisa ter acesso ao sitema, token de autenticação e dispositivo registrado

import requests
import json


class CasoUsoExemplo1:
    def __init__(self, token, device_serial):
        self.urlbase = 'https://plataformaiotalfa.herokuapp.com/api/v1/'
        # self.urlbase = 'http://127.0.0.1:8000/api/v1/'
        self.authtoken = str(token)
        self.device_serial = str(device_serial)
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Token {self.authtoken}'}
        self.deviceData = None

    def getDevice(self):
        url = f'{self.urlbase}dispositivos/{self.device_serial}/'
        request = requests.get(url=url, headers=self.headers)
        if request.status_code == 200:
            self.deviceData = request.json()

    def getAllDatas(self):
        dados = self.deviceData[0]['dados']
        return dados

    def getConfigurations(self):
        confs = self.deviceData[0]['configuracoes'][0]
        return confs

    def getMessages(self):
        msgs = self.deviceData[0]['mensagens']
        return msgs

    def sendData(self, data, unidade):
        body = {"Media type": "application/json", "unidade": unidade, "dado": data}
        json_body = json.dumps(body)
        url = f'{self.urlbase}dados/{self.device_serial}/'
        request = requests.post(url=url, headers=self.headers, data=json_body)
        print(request.text)
        if request.status_code == 201:
            return request.json()

    def sendMessage(self, alerttitle, msg, critc):
        body = {"Media type": "application/json", "alerta": alerttitle, "mensagem": msg, "is_critic": str(critc)}
        json_body = json.dumps(body)
        url = f'{self.urlbase}mensagens/{self.device_serial}/'
        request = requests.post(url=url, headers=self.headers, data=json_body)
        print(request.text)
        if request.status_code == 201:
            return request.json()


# Descomente o código abaixo para testar a API
# teste = CasoUsoExemplo1('seu token', 'serial do dispositivo')
# teste.getDevice()
# print(teste.deviceData)
# print(teste.getConfigurations())
# print(teste.getAllDatas())
# print(teste.getMessages())
# teste.sendData(15, 'u.d')
# teste.getDevice()
# teste.sendMessage('dipositivo atualizado', 'dados atualizados no sitema', False)
# print(teste.getAllDatas())
# print(teste.getMessages())
# teste.sendMessage('dispositivo desligado', 'sistema interrompeu dispositivo', True)
# teste.getDevice()
# print(teste.getMessages())
