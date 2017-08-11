import smtplib
import time
import imaplib
import email
from bs4 import BeautifulSoup
import re
from flask import Flask , jsonify, abort, make_response, request
import httplib2
import json
from datetime import datetime
from dateutil.tz import tzoffset

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow



# these are generated for the account
client_id = '1006875010209-bs2h0kgmckohh2cilcldndmu8t8fvj0t.apps.googleusercontent.com'
client_secret = 'lw0l3rtYjb1dfI0J1W5KXL46'

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

# Declare the email and its credentials
ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "roamworkstech" + ORG_EMAIL
FROM_PWD    = "Tom@RW1206"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# A class is declared to interact with the calendar item obtained from api call
class calendar_item():
    kind ='calendar#calendarListEntry'


# A class is declared to interact with the event items obtained from api call
class event_item():
    kind = 'calendar#event'
    # function to save event data into class object
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

    # function to show data stored as class object
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



# function to build a json object when keys and values are passed
def build_json(keys = [],values = []):
    length = len(keys)
    data = {}
    for i in range(length):
        keyitem = keys[i]
        valuitem = values[i]
        data[keyitem]= valuitem
    this_json = json.dumps(data)
    json_data = json.loads(this_json)
    return json_data

def read_calendars():

    service=init_google_service_call()
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # print (calendar_list_entry['summary'])
            # print (calendar_list_entry['id'])
            # print(calendar_list_entry['kind'])
            keys=['summary','id','kind']
            values=[calendar_list_entry['summary'],calendar_list_entry['id'],calendar_list_entry['kind']]
            print(build_json(keys,values))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


# function to create an event.

def read_events(calendarId):
    my_calendarId=calendarId
    service=init_google_service_call()
    print ("Reading events")
    #read all calendars from the authorized user






    try:

        # The Calendar API's events().list method returns paginated results, so we
        # have to execute the request in a paging loop. First, build the
        # request object. The arguments provided are:
        #   primary calendar for user
        request = service.events().list(calendarId=my_calendarId)
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


def create_event(calendarId,eventItem):
    thisCalendarId=calendarId
    thisEventItem=eventItem
    service=init_google_service_call()
    print('Create an event')
    created_event = service.events().insert(calendarId=thisCalendarId,body=thisEventItem).execute()
    created_event_class = event_item(created_event)
    created_event_class.show_event()

def update_event(calendarId,eventId,eventItem):

    thisCalendarId=calendarId
    thisEventId=eventId
    thisEventItem=json.loads(eventItem)
    service=init_google_service_call()
    print('gathering event with provided EventID and CalendarID')

    event = service.events().get(calendarId=thisCalendarId, eventId=thisEventId).execute()
    my_event_item = event_item(event)
    my_event_item.show_event()
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=thisEventItem).execute()

    # Print the updated date.
    updated_event_class = event_item(updated_event)
    updated_event_class.show_event()



def init_google_service_call():
    # Create a flow object. This object holds the client_id, client_secret, and
    # scope. It assists with OAuth 2.0 steps to get user authorization and
    # credentials.
    flow = OAuth2WebServerFlow(client_id, client_secret, scope)

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

    return service


def read_emails2json():
     try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
            # print(mail.list()) # prints the folders
        mail.select('inbox')


        result, data = mail.uid('search', None, "UNSEEN") # search and return uids instead
        email_count = (len(list(data[0].split())))
        print ("Total Unread emails "+ str(email_count))
        if (email_count>0):
            latest_email_uid = data[0].split()[-1]

            #print((data[0][1]))
            uid_list = data[0].decode("utf-8", "ignore").split()
            print (uid_list)

            for i in range (len(list(data[0].split()))):
                email_uid = uid_list[i]
                result, data = mail.uid('fetch', email_uid, '(RFC822)')
                raw_email = data[0][1]

                email_message=email.message_from_bytes(raw_email)

                sender = email_message['from']
                receipient  = email_message['to']
                cc = email_message['cc']
                bcc = email_message['bcc']
                #similar to subject get only the date , strip all metadata
                a = email_message['Received']
                a = a.strip(',.-')
                a = a.replace('  ','')

                received_on = a[a.find(",")-3:a.find("-")]
                received_on.strip()

                subject = email_message['subject']
                #because subject may contain additional metadata , strip them , and shorten the subject
                if len(subject) > 300 :
                    subject = subject[:299]
                subject = subject.replace('=','')
                subject = subject.replace('?','')

                for part in email_message.walk():
                    body_str=''

                    if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html" :
                            #try various encodings
                            encodings =[part.get_content_charset(),'ISO-8859-1','UTF-8','Windows-1252']
                            for encoding in encodings :
                                try:

                                   body_bytes = part.get_payload(decode=True)
                                   body_str = body_bytes.decode(encoding)
                                   soup = BeautifulSoup(body_str,"html.parser")
                                   body = soup.get_text()
                                   body = re.sub(r'<.*?>', '', body)
                                except Exception:
                                    pass


                    if part.get_content_maintype() == 'multipart':
                        pass

                    if part.get('Content-Disposition') is None:
                        pass


                #print("FROM:"+sender)
                #print("SUBJECT:"+subject)
                #print("TO:"+receipient)
                #if cc != None:
                #    print("CC:"+ cc)
                #print("DATE:"+received_on)
                #print("Body_HTML:"+body_str)
                #print("Body_Simple:"+str(body))


                #build a json object from each read email
                keys = ['from','subject','to','date','bodyHtml','bodySimple']
                values = [sender,subject,receipient,received_on,body_str,body]
                data = build_json(keys,values)

                # call a email parser to work with the read email
                parse_json_email(data)
     except:
         print ("Error Occured")
         pass

#
def parse_json_email(data):
    this_json = json.loads(data)
    keeys = list(this_json.keys())
    valluees = list(this_json.values())

    if 'subject' in keeys :
        cursor = keeys.index('subject')
        value = valluees[cursor]

        # process emails that have #cal#parasql as subject
        if value == '#cal#parasql':
            print ('ParaSQL calendar entry')
            # call a function to build an event from the HTML Body of the email
            event_reqestlist = build_event_fromEmail(this_json['bodyHtml'])
            print(event_reqestlist)
            event = create_event_json(event_reqestlist[0],event_reqestlist[1],event_reqestlist[2],event_reqestlist[3],event_reqestlist[4])
            print(event)
            # creating events
            #create_event('roamworkstech@gmail.com',event)


def build_event_fromEmail(text):
    print(text)
    techname = 'none'
    agentname = 'none'
    date = 'none'
    location = 'none'
    type = 'none'
    newtext=text.split("<br>")
    str_list = list(filter(None, newtext))
    information_list = []
    for i in range(len (str_list)):
        if (str_list[0] == "Calendar Entry" and i>0):
            cursor = str_list[i].index(':')
            information_list.append(str_list[i][cursor+2:])

    return information_list

# create_event_json creates a json object that can be passed as event object to a create or update (id needs to be found)
def create_event_json(visittype,location, techname,agentname, startdate):
    date_startdate = datetime.strptime(startdate, "%Y-%m-%d").date()
    year = date_startdate.year
    month = date_startdate.month
    day = date_startdate.day
    startdatetimestamp = datetime(year, month, day, 10, 0, tzinfo=tzoffset('None', +14400))
    enddatetimestamp = datetime(year, month, day, 14, 0, tzinfo=tzoffset('None', +14400))
    event = {
        'summary': visittype + " for " + techname,
        'location': location,
        'description': agentname + " scheduled " + visittype + " for " + techname + " at " + location + " for " + startdate,
        'start': {
              'dateTime': str(startdatetimestamp).replace(' ','T'),
          },
        'end': {
              'dateTime': str(enddatetimestamp).replace(' ','T'),
          },
      }

    print (event)
    return event



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

    # function to read all calendars
    # read_calendars()

    # function to read all entries
    read_events('roamworkstech@gmail.com')

    # function to update event
    # calendarId='primary'
    # eventId='op9gi0g74ldbcup78clts42ijo'
    # eventItem=create_event_json(techname, location, visittype, agentname, startdate)
    # update_event(calendarId,eventId,eventItem)

    # function to read all emails
    read_emails2json()

if __name__ == '__main__':
  main()

