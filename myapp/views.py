from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_CALENDAR_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, _ = flow.authorization_url(access_type='offline')
    return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    code = request.GET.get('code')
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_CALENDAR_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials

    service = build('calendar', 'v3', credentials=credentials)
    events = service.events().list(calendarId='primary').execute()

    # Process the events or return the events list as a response
    return HttpResponse(events)
