# Template utilizado para envio de mensagens informando o status de rejeição para uma requisição feita pelo aluno tutor sobre um conteúdo de sua autoria

default_message = '''\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Abandono de conteúdo</title>
</head>
<body>
    <table cellpadding="0" cellspacing="0" width="100%">
        <tbody>
            <tr align="center">
                <td>
                    <img src="https://ifstudy-bucket.s3.amazonaws.com/logo_branco.svg">
                </td>
            </tr>
            <tr align="center">
                <td>
                    <table style="width:100%; max-width:560px; height:124px; background-color:#3D3D3D">
                        <tbody>
                            <tr>
                                <td style="padding-left:32px">
                                    <font style="font-size:20px; font-weight:bold; font-stretch:normal; font-style:normal; line-height:normal; font-family: Arial; letter-spacing:normal; color:#ffffff">
                                        Comunidade IF-Study 
                                    </font>
                                </td>
                                <td style="text-align:end; padding-right:14px;">
                                    <img data-imagetype="External" src="https://ifstudy-bucket.s3.amazonaws.com/atendente.svg" > 
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td align="center">
                    <br/>
                    <!-- Título -->
                    <font style="font-size:19px; font-family: Arial; font-weight:bold;">
                        Faz tempo que não te vemos!
                    </font>
                </td>
            </tr>
            <tr>
                <td align="center">
                    <table style="width:100%; max-width:560px; height:124px;">
                        <tbody>
                            <tr>
                                <!-- Corpo da mensagem -->
                                <td style="padding-left:32px; font-family: Arial;">
                                    <p><strong>Reparamos que você está há um tempo sem utilizar o IF-Study</strong></p> 
                                    <p>Existem sempre novas trilhas a serem criadas e novos assuntos para aprender</p>
                                    <p>Ou que tal compartilhar algum conteúdo com algo novo que você aprendeu?</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
            <td align="center">
                <br/>
                <table style="width:100%; max-width:560px; height:124px;">
                    <tbody>
                        <tr>
                            <td style="width:100%; border-radius:4px; background-color:#ececec; padding:16px; text-align:center">
                                <font style="font-size:14px; font-family: Arial; font-weight:normal; font-stretch:normal; font-style:normal; line-height:1.14; letter-spacing:normal; color:#757575">
                                    Esta mensagem foi enviada a você pela equipe de Administração do IF-Study. Se você acha que esta mensagem não é para você, ignore este e-mail. 
                                </font>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
            </tr>
        </tbody>
    </table>
</body>
</html>'''