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
    context = {}
    creds = None
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir,'client_secret_esadb.json')
    token_path = os.path.join(home_dir,'token_esadb.json')
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        # Call the Drive v3 API
        results = service.files().list(fields="files(id, name)").execute()
        items = results.get('files', [])
        context['filelist'] = items
    except HttpError as error:
        context['status'] = error
    return render(request, 'gdisk_list.html', context = context)




