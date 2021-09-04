# Caso de uso básico para exemplificar o uso da API em apenas 1 dispositivo
# antes de tudo voce precisa ter acesso ao sitema, token de autenticação e dispositivo registrado

import requests


class CasoUsoExemplo1:
    def __init__(self, token, device_id):
        self.urlbase = 'https://plataformaiotalfa.herokuapp.com/api/v1/'
        self.authtoken = str(token)
        self.device_id = str(device_id)
        self.headers = {'Authorization': f'Token {self.authtoken}'}
        self.deviceData = None

    def getDevice(self):
        url = f'{self.urlbase}dispositivos/{self.device_id}'
        request = requests.get(url=url, headers=self.headers)
        self.deviceData = request.json()

    def getAllDatas(self):
        dados = self.deviceData['dados']
        return dados

    def getConfigurations(self):
        confs = self.deviceData['configuracoes'][0]
        return confs

    def getMessages(self):
        msgs = self.deviceData['mensagens']
        return msgs

    def sendData(self, data):
        return

    def sendMessage(self, alerttitle, msg):
        return
