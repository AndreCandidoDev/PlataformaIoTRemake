import requests
import json


class PlataformLib:
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
            return self.deviceData
        else:
            raise Exception(f'Error {request.status_code}, {request.text}')

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
        if request.status_code == 201:
            return request.json()
        else:
            raise Exception(f'Error {request.status_code}, {request.text}')

    def sendMessage(self, alerttitle, msg, critc):
        body = {"Media type": "application/json", "alerta": alerttitle, "mensagem": msg, "is_critic": str(critc)}
        json_body = json.dumps(body)
        url = f'{self.urlbase}mensagens/{self.device_serial}/'
        request = requests.post(url=url, headers=self.headers, data=json_body)
        if request.status_code == 201:
            return request.json()
        else:
            raise Exception(f'Error {request.status_code}, {request.text}')
