import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .interfaces import Sender

class SmtpSender(Sender):
    """Implementação de envio de e-mail via SMTP"""
    def __init__(self):
        self.server_email = "ifstudy.correio.digital.dev@gmail.com"
        self.server_port = 465
        self.password = os.getenv("SMTP_EMAIL_PASS")

    def enviar(self, remetente:str, destinatarios:list, assunto:str, mensagem:str):
        try:
            email = MIMEMultipart("alternative")
            email["Subject"] = assunto
            email["From"] = remetente
            email["To"] = ', '.join(destinatarios)
            mensagem_mime = MIMEText(mensagem, "html")
            email.attach(mensagem_mime)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", self.server_port, context=context) as server:
                server.login(self.server_email, self.password)
                server.sendmail(remetente, destinatarios, email.as_string())         
            print("E-mail enviado com sucesso")
        except smtplib.SMTPException as exception:
            print(exception)
            print("Falha no envio do E-mail")