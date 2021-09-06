# Nesse exemplo será simulado o envio de dados e criação de alertas, tudo será visualizado no analitycs

from IoTLib import PlataformLib
import random


def gerador(minvalue, maxvalue):
    return random.randint(minvalue, maxvalue)


# obtenha seu token de autenticação e crie 5 dispositivos e atribua as variaveis a seguir seus valores
authtoken = 'Seu token de autenticação'
d1 = PlataformLib(authtoken, 'Serial do 1° dispositivo')
d2 = PlataformLib(authtoken, 'Serial do 2° dispositivo')
d3 = PlataformLib(authtoken, 'Serial do 3° dispositivo')
d4 = PlataformLib(authtoken, 'Serial do 4° dispositivo')
d5 = PlataformLib(authtoken, 'Serial do 5° dispositivo')

devices = [d1, d2, d3, d4, d5]
cont = 0
while cont <= 9:
    print("=============== Simulando recepcao de dados ============================")
    for i in devices:
        dispositivo = i.getDevice()
        dado = gerador(10, 40)
        print('Valor obtido', dado)
        limites = dispositivo[0]['configuracoes'][0]
        inf = int(limites['limite_inferior'])
        sup = int(limites['limite_superior'])
        i.sendData(dado, 'unidade generica')
        if dado < inf or dado > sup:
            print('Valor fora da faixa de limite')
            i.sendMessage('Valor fora da faixa', f'Valor lido: {dado}', critc=True)
        else:
            i.sendMessage('Tudo Ok', 'Leitura sem problemas', critc=False)
        print("=======================================================================\n")
        print("Acessando o dipositivo...")
        dispositivo = i.getDevice()
        print('Dados: ', i.getAllDatas())
        print('Mensagens: ', i.getMessages())
        print('=======================================================================\n')
    cont += 1
