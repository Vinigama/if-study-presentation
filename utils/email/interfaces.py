import abc

class Sender:
    """Classe abstrata que faz a interface para os envios de e-mail"""
    __metaclass__  = abc.ABCMeta

    @abc.abstractclassmethod
    def enviar(self, remetente:str, destinarios: list, assunto:str, mensagem: str):
        return 