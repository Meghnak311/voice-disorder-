import os

from twilio.rest import Client


def send_sms(content):
    account_sid = 'ACb41ccb3fa2539480d341653fcf8a3c41'
    auth_token = 'e542589fc1a09cf30c259e4df372113b'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=content,
        from_='+19786482209',
        to='+917510310639'
    )
    print('message sent')
