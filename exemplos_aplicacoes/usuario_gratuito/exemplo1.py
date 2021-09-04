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
        if request.status_code == 200:
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

    def sendData(self, data, unidade):
        nome = self.deviceData['id']
        body = {"dispositivo": nome, "unidade": unidade, "dado": data}
        url = f'{self.urlbase}dados/'
        request = requests.post(url=url, headers=self.headers, data=body)
        if request.status_code == 201:
            return request.json()

    def sendMessage(self, alerttitle, msg, critc):
        print(critc)
        nome = self.deviceData['id']
        body = {"dispositivo": nome, "alerta": alerttitle, "mensagem": msg, "is_critic": str(critc)}
        url = f'{self.urlbase}mensagens/'
        request = requests.post(url=url, headers=self.headers, data=body)
        if request.status_code == 201:
            return request.json()


# Descomente o código abaixo para testar a API
# teste = CasoUsoExemplo1('seu token', id do dispositivo)
# teste.getDevice()
# print(teste.deviceData)
# print(teste.getConfigurations())
# print(teste.getAllDatas())
# print(teste.getMessages())
# teste.sendData(19, 'u.d')
# teste.getDevice()
# teste.sendMessage('dipositivo atualizado', 'dados atualizados no sitema', False)
# print(teste.getAllDatas())
# print(teste.getMessages())
# teste.sendMessage('dispositivo desligado', 'sistema interrompeu dispositivo', True)
# teste.getDevice()
# print(teste.getMessages())
