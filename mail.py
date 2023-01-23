import base64
import math
import mimetypes
import os
from email.message import EmailMessage
from random import random
from time import sleep

from google.oauth2.credentials import Credentials
from google.auth.transport import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from data import data, data_spot

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def get_cred():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def gmail_create_draft_with_attachment(service, to, name):
    """Create and insert a draft email with attachment.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """

    try:
        # create gmail api client
        mime_message = EmailMessage()

        # headers
        mime_message['To'] = to
        mime_message['From'] = 'sasthrayaan@cusat.ac.in'
        mime_message['Subject'] = 'Sasthrayaan Participation Certificate'

        # text
        mime_message.set_content(
            f'Hi, {name.title()}\n\n'
            '   Thank you for participating in Sasthrayaan 2023.'
            'Please find the attached the Certificate of Participation.\n\n'
            'Regards, \n'
            'Team Sasthrayaan'
        )

        # attachment
        attachment_filename = f'out/{to}.png'
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split('/')

        with open(attachment_filename, 'rb') as fp:
            attachment_data = fp.read()

        mime_message.add_attachment(attachment_data, maintype, subtype)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None

    return send_message


def main():
    creds = get_cred()
    service = build('gmail', 'v1', credentials=creds)

    print('Sending emails... ' + str(len(data_spot)))

    for email, name in data_spot:
        print(email)
        gmail_create_draft_with_attachment(service, email, name)
        sleep(random() * 2)


if __name__ == '__main__':
    main()
