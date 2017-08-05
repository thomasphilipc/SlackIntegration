from oauth2client import client, file, tools
from httplib2 Http
from googleapiclient import discovery

flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://example.com/auth_return')


GCAL = discovery.build('calendar', 'v3',http=creds.authorize(Http()))