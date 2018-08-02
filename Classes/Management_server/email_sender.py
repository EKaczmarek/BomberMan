import smtplib

from email.message import EmailMessage

import requests


SENDER = {
    'login': '',
    'password': '',
    'from': '',
}


def _create_account_activation_url(activation_params):
    activation_url = 'http://localhost:9090/activate/'
    return requests.Request('GET', activation_url, params=activation_params).prepare().url


def _create_account_activation_message(player):
    activation_params = {k: v for k, v in player.items() if k in ('nickname', 'activation_key')}
    message = EmailMessage()
    message.set_content('To activate your account, {}, use this link: {}'.format(
        player['nickname'], _create_account_activation_url(activation_params)))
    message['Subject'] = 'Account activation'
    message['To'] = player['email']
    return message


def _send_mail_via_gmail(sender, receivers, message):
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp_server:
        smtp_server.set_debuglevel(2)
        smtp_server.starttls()
        smtp_server.login(sender['login'], sender['password'])
        smtp_server.sendmail(sender['from'], receivers, message)


def send_account_activation_mail(player):
    send_mail = _send_mail_via_gmail
    account_activation_message = _create_account_activation_message(player)
    account_activation_message['From'] = SENDER['from']
    send_mail(SENDER, account_activation_message['To'], account_activation_message.as_string())