import httplib2
import json
import sys
from dateutil.tz import tzoffset
from datetime import datetime
from dateutil.tz import tzoffset

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

class calendar_item():
    kind ='calendar#calendarListEntry'

class event_item():
    kind = 'calendar#event'
    def __init__(self,event):
        if (self.kind == event.get('kind')):
            self.kind = event.get('kind')
            self.id = event.get('id')
            self.summary = event.get('summary')
            self.description = event.get('description')
            self.location = event.get('location')
            self.htmlLink = event.get('htmlLink')
            eventstartvar = event.get('start')
            self.startDateTime = eventstartvar.get('dateTime')
            eventendvar = event.get('end')
            self.endDateTime = eventendvar.get('dateTime')
            self.created = event.get('created')
            self.updated = event.get('updated')
            self.status = event.get('status')

    def show_event(self):
            print('Kind: '+self.kind)
            print('Id: '+self.id)
            print('Summary: '+self.summary)
            print('Description: '+str(self.description))
            print('Location: '+self.location)
            print('HTML Link: '+self.htmlLink )
            print('Starting: '+self.startDateTime )
            print('Ending: '+self.endDateTime)
            print('Created: '+self.created )
            print('Updated: '+self.updated)
            print('Status : '+self.status)



# these are generated for the account
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


def create_event():
    print('Create an event')


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
    credentials = tools.run_flow(flow, storage)

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

  newevent = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
  },
}

  #to add event uncomment below 3 lines
  new_event=create_event_json('tech', 'location', 'installation', 'testSupportAgent', '2017-09-12')
  event = service.events().insert(calendarId='primary',body=new_event).execute()
  print('Event created: {}'.format(event.get('htmlLink')))


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
        this_event_item = event_item(event)

        this_event_item.show_event()
        print ('---------------------------------------')
      # Get the next request object by passing the previous request object to
      # the list_next method.
      request = service.events().list_next(request, response)

  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')

  event = service.events().get(calendarId='primary', eventId='op9gi0g74ldbcup78clts42ijo').execute()

  #event['summary'] = 'QER - HEMS'
  event['start.dateTime']='2017-08-07T09:00:00-06:00'


  #updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    # Print the updated date.
  #print (updated_event['updated'])

def create_event_json(techname, location, visittype, agentname, startdate):
    date_startdate = datetime.strptime(startdate, "%Y-%m-%d").date()
    year = date_startdate.year
    month = date_startdate.month
    day = date_startdate.day
    startdatetimestamp = datetime(year, month, day, 10, 0, tzinfo=tzoffset('None', +14400))
    enddatetimestamp = datetime(year, month, day, 14, 0, tzinfo=tzoffset('None', +14400))
    print('Start time: ' + str(startdatetimestamp))
    print('End time: ' + str(enddatetimestamp))
    event = {
        'summary': visittype + " by " + techname,
        'location': location,
        'description': agentname + " scheduled " + visittype + " by " + techname + " at " + location + " for " + startdate,
        'start': {
              'dateTime': str(startdatetimestamp).replace(' ','T'),
          },
        'end': {
              'dateTime': str(enddatetimestamp).replace(' ','T'),
          },
      }

    return event




if __name__ == '__main__':
  main()