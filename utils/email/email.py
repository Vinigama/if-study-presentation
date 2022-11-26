from sys import implementation


from .implementations import SmtpSender

class EmailSender:
    """Classe utilitária para envio de e-mails"""

    def __init__(self, remetente:str, destinatarios:list, assunto:str, mensagem:str):
        self.remetente = remetente
        self.destinatarios = destinatarios
        self.assunto = assunto
        self.mensagem = mensagem
        self.senderImpl = SmtpSender() # Implementação Padrão

    def enviar(self):
        self.senderImpl.enviar(
            self.remetente,
            self.destinatarios,
            self.assunto,
            self.mensagem)