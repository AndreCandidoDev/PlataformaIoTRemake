import statistics


class Estatisticas:
    def __init__(self, dados):
        self.dados = dados
        self.dates = dados
        self.flag_error = False

    def conv_data_to_string(self):
        aux = []
        for i in self.dados:
            aux.append(float(i.dado))
        return aux

    def conv_datetime_to_string(self):
        aux = []
        for i in self.dates:
            datas = str(i.criacao)
            conv = datas.split(' ')
            hora_format = conv[1].split('.')[0]
            aux.append(f'{conv[0]}-{hora_format}')
        return aux

    def error(self):
        dates = self.conv_datetime_to_string()
        self.flag_error = True
        return dates

    def media(self):
        try:  # calcula para dados numericos
            self.dados = self.conv_data_to_string()
            return statistics.mean(self.dados)
        except:  # mostra quantas leituras foram obtidas
            return self.error()

    def mediana(self):
        if self.flag_error:
            pass
        else:
            return statistics.median(self.dados)

    def moda(self):
        if self.flag_error:
            pass
        else:
            return statistics.mode(self.dados)
