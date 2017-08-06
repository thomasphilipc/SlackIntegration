import httplib2
import json
import sys

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

# For this example, the client id and client secret are command-line arguments.
client_id = '1006875010209-bs2h0kgmckohh2cilcldndmu8t8fvj0t.apps.googleusercontent.com'
client_secret = 'lw0l3rtYjb1dfI0J1W5KXL46'

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

def build_json(keys = [],values = []):
    length = len(keys)
    data = {}
    for i in range(length):
        keyitem = keys[i]
        valuitem = values[i]
        data[keyitem]= valuitem
    json_data = json.dumps(data)
    return json_data


def main():

  # Create a Storage object. This object holds the credentials that your
  # application needs to authorize access to the user's data. The name of the
  # credentials file is provided. If the file does not exist, it is
  # created. This object can only hold credentials for a single user, so
  # as-written, this script can only handle a single user.
  storage = Storage('credentials.dat')

  # The get() function returns the credentials for the Storage object. If no
  # credentials were found, None is returned.
  credentials = storage.get()

  # If no credentials are found or the credentials are invalid due to
  # expiration, new credentials need to be obtained from the authorization
  # server. The oauth2client.tools.run_flow() function attempts to open an
  # authorization server page in your default web browser. The server
  # asks the user to grant your application access to the user's data.
  # If the user grants access, the run_flow() function returns new credentials.
  # The new credentials are also stored in the supplied Storage object,
  # which updates the credentials.dat file.
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

  # Create an httplib2.Http object to handle our HTTP requests, and authorize it
  # using the credentials.authorize() function.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the calendar API. The arguments provided are:
  #   name of the API ('calendar')
  #   version of the API you are using ('v3')
  #   authorized httplib2.Http() object that can be used for API calls
  service = build('calendar', 'v3', http=http)



  event = {
  'summary': 'Test Event',
  'location': 'QER - Jebel Ali',
  'description': 'Profiling HEMS equipment.',
  'start': {
    'dateTime': '2017-08-06T09:00:00-07:00',
  },
  'end': {
    'dateTime': '2017-08-06T17:00:00-07:00',
  },
  'attendees': [
    {'email': 'talk2tpc@gmail.com'},
    {'email': 'thomasphilip.c@gmail.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        print (calendar_list_entry['summary'])
        print (calendar_list_entry['id'])
        print(calendar_list_entry['kind'])
        keys=['summary','id','kind']
        values=[calendar_list_entry['summary'],calendar_list_entry['id'],calendar_list_entry['kind']]
        print(build_json(keys,values))
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
        break

  calendar_list_entry = service.calendarList().get(calendarId='roamworkstech@gmail.com').execute()

  print (calendar_list_entry['summary'])

  #to add event uncomment below 2 lines
  #event = service.events().insert(calendarId='primary',body=event).execute()
  #print('Event created: {}'.format(event.get('htmlLink')))
  try:

    # The Calendar API's events().list method returns paginated results, so we
    # have to execute the request in a paging loop. First, build the
    # request object. The arguments provided are:
    #   primary calendar for user
    request = service.events().list(calendarId='roamworkstech@gmail.com')
    # Loop until all pages have been processed.
    while request != None:
      # Get the next page.
      response = request.execute()
      # Accessing the response like a dict object with an 'items' key
      # returns a list of item objects (events).
      for event in response.get('items', []):
        # The event object is a dict object with a 'summary' key.
        print (repr(event.get('id', 'NO ID')))
        print (repr(event.get('summary', 'NO SUMMARY')))
        print (repr(event.get('description' , 'NO DESCP')))
        print (repr(event.get('location' , 'NO location')))
        print (repr(event.get('htmlLink' , 'NO Link')))
        print (repr(event.get('kind' , 'NO Kind')))
        print (repr(event.get('originalStartTime.dateTime' , 'NO start date')))
        print (repr(event.get('updated' , 'NO udpates')))
        print ('---------------------------------------')
      # Get the next request object by passing the previous request object to
      # the list_next method.
      request = service.events().list_next(request, response)

  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')

  event = service.events().get(calendarId='primary', eventId='8l7iga12h87bd42nev1kqqm0bk').execute()

  event['summary'] = 'QER - HEMS'
  event['OriginalStartTime.dateTime']='2017-08-05T06:05:03.884Z'

  #updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    # Print the updated date.
  #print (updated_event['updated'])

if __name__ == '__main__':
  main()