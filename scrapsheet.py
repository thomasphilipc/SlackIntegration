from dateutil.tz import tzoffset
from datetime import datetime

def create_event_json(techname, location, visittype, agentname, startdate):
    date_startdate=datetime.strptime(startdate, "%Y-%m-%d").date()
    year=date_startdate.year
    month=date_startdate.month
    day=date_startdate.day
    startdatetimestamp= datetime(year, month, day, 10, 0, tzinfo=tzoffset('None', +14400))
    enddatetimestamp=datetime(year, month, day, 14, 0, tzinfo=tzoffset('None', +14400))
    print( 'Start time: '+ str(startdatetimestamp))
    print ('End time: '+str(enddatetimestamp))
    event = {
        'summary': visittype + "by" + techname ,
        'location': location ,
        'description': agentname + " scheduled " + visittype + " by " + techname + " at " + location + " for " + startdate ,
        'start': {
            'dateTime': startdatetimestamp,
        },
        'end': {
            'dateTime': enddatetimestamp,
        },
    }

    return event


print(create_event_json('testtech','testlocation','installation','ibrahim','2017-08-03'))