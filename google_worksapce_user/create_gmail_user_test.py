from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import random
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.user.security']

def main():
    #Credentials Directory API connected from the gcp account dmytrii.brovko@dev.pro
    account_secret = 'credentials.json'
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
                account_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        #with open('token.json', 'w') as token:
        #  token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    # New User credentials
    name = input('What is the new user Name and Surname ? "example: alexsandra lein" (*no case sensitive) :').title().split()

    password = input('Generate a password automatically ? y/n : ')
    while not (password == 'y' or password == 'yes' or password == 'n' or password == 'no' or password == 'not'):
       password = input('Generate a password automatically ? y/n : ')
    if (password == 'y' or password == 'yes'):
        password = ''
        for i in range(12):
          password += random.choice('+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    else: 
       password = input('Enter a password for new user :')

    groups = input('What is Gsuite Groups that user should be added *** (enter group email) ***? :').lower().split()
    email = "{}.{}@gcg-trust.com".format(name[0], name[1])
    fullname = name[0] + " " + name[1]
    userinfo = {
        "password": password,
        "primaryEmail": email,
        "name": {
            "familyName": name[1],
            "givenName": name[0],
            "fullName": fullname
        },
        "changePasswordAtNextLogin": "false"
    }

    groupinfo = {
        "email": email,
        "role": "MEMBER"
    }

    # Create User
    service.users().insert(body=userinfo).execute()
  
    # Add User to group
    add_group = []
    for x in groups:
        try:
          service.members().insert(groupKey=x, body=groupinfo).execute()
          time.sleep(1)
          service.members().get(groupKey=x, memberKey=email).execute()
          add_group.append(x)
        except:
            pass

    print("New user email and password :" + email.lower() + " " + password)
    print("New user added in {} groups".format(add_group))
    time.sleep(12321321)

    # Create signature
    # SCOP = ['https://www.googleapis.com/auth/gmail.settings.basic',
    #        'https://www.googleapis.com/auth/gmail.settings.sharing']
    #
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     account_secret, SCOPES)
    # new_creds = flow.run_local_server(port=0)
    #
    # position = input('What is the new user Position ? :')
    # city = input('What is the new user City ? :')
    # phone = input('What is the new user Phone ? (+380507788999):')
    #
    #
    # newPhone = '+{} ({}) {}-{}'.format(phone[0:3], phone[3:5], phone[5:8], phone[8:12])
    #
    # DATA  = {
    #    'signature': "  \
    #         <b>&mdash; <br> \
    #         <font color=#6AA84F>{}</font><br> \
    #         {} [{}]<br></b> \
    #         {}<br>\
    #         skype: {} (Dev.Pro)<br> \
    #         <b><a href='https://dev.pro'>dev.pro</a>".format(fullname, position, city, newPhone, fullname)
    # }
    # GMAIL = build('gmail', 'v1', credentials=creds)
    #
    # addresses = GMAIL.users().settings().sendAs().list(userId=email, fields='sendAs(isPrimary,sendAsEmail)').execute().get('sendAs', [])
    # for addresses in addresses:
    #    if addresses['isPrimary']:
    #        break
    #
    # rsp = GMAIL.users().settings().sendAs().patch(userId=email, sendAsEmail=addresses['sendAsEmail'], body=DATA).execute()
    # print("Primary address signature changed")

if __name__ == '__main__':
    main()