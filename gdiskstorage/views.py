import os
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

# Google drive API modules
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

@require_http_methods(['GET'])
def gdisk_list(request):
    try:
        creds = Credentials.from_authorized_user_file('client_secret_esadb.json', SCOPES)
        service = build('drive', 'v3', credentials = creds)
        filelist = service.files()
    except BaseException as error:
        filelist = []
        error = 'secret json problem in ' + os.getcwd()
    finally:
        context = {'status': error,
        'subtitle':'Медиа: Google drive'}
        context['filelist'] = filelist
        return render(request, 'gdisk_list.html', context = context)




