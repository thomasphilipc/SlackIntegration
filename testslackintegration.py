from flask import Flask , jsonify, abort, make_response, request
from flask import render_template
import requests
import json
import _thread
import time


app= Flask(__name__)

class slack_slash_command:
    token = None
    team_id = None
    team_domain = None
    enterprise_id = None
    enterprise_name = None
    channel_id = None
    channel_name = None
    user_id = None
    user_name = None
    command = None
    text = None
    response_url = None

    def __init__(self,request):

        cursor = 0
        print ('entered command initializaiton')

        #obtain the json passed
        keeys = list(request.form.keys())
        valluees = list(request.form.values())
        # printing the json for log purposes
        print ('Below is the json payload for a slack command')
        for i in range(len(keeys)):
            print(keeys[i] + " contains " + valluees[i])

        # checking existence of data and assigning the value
        if 'token' in keeys:
            cursor = keeys.index('token')
            self.token = valluees[cursor]

        if 'team_id' in keeys:
            cursor = keeys.index('team_id')
            self.team_id = valluees[cursor]

        if 'team_domain' in keeys:
            cursor = keeys.index('team_domain')
            self.team_domain = valluees[cursor]

        if 'channel_id' in keeys:
            cursor = keeys.index('channel_id')
            self.channel_id = valluees[cursor]

        if 'channel_name' in keeys:
            cursor = keeys.index('channel_name')
            self.channel_name = valluees[cursor]

        if 'user_id' in keeys:
            cursor = keeys.index('user_id')
            self.user_id = valluees[cursor]

        if 'user_name' in keeys:
            cursor = keeys.index('user_name')
            self.user_name = valluees[cursor]

        if 'command' in keeys:
            cursor = keeys.index('command')
            self.command = valluees[cursor]

        if 'text' in keeys:
            cursor = keeys.index('text')
            self.text = valluees[cursor]

        if 'response_url' in keeys:
            cursor = keeys.index('response_url')
            self.response_url = valluees[cursor]

        if 'trigger_id' in keeys:
            cursor = keeys.index('trigger_id')
            self.trigger_id = valluees[cursor]


class slack_slash_response_command:

    token = None
    team_id = None
    team_domain = None
    channel_id = None
    channel_name = None
    user_id = None
    user_name = None
    action_name = None
    action_type = None
    action_value = None
    callback_id = None
    response_url = None
    action_ts = None
    message_ts = None
    attachment_id = None
    is_app_unfurl = None
    trigger_id = None

    def __init__(self,request):
        print ('Entered slash response initialization')

        keeys = list(request.form.keys())
        valluees = list(request.form.values())
        # printing the json for log purposes
        print(' Total number of entries on response is {}'.format(len(keeys)))
        for i in range (len(keeys)):
            print(keeys[i] + " contains " + valluees[i])

        workablejson = valluees[0]
        data = json.loads(workablejson)

        print('Actions contain {}'.format(data['actions']))
        dataactionlist = list (data['actions'])
        print('There is a total of () entries in actions'.format(len(dataactionlist)))
        for i in range(len(dataactionlist)):
            actiondata = dataactionlist[i]
            print (actiondata)
            if 'value' in actiondata.keys():
                print('action_value is {}'.format(actiondata['value']))
                self.action_value = actiondata['value']
            if 'type' in actiondata.keys():
                print('action_type is {}'.format(actiondata['type']))
                self.action_type = actiondata['type']
            if 'name' in actiondata.keys():
                print('action_name is {}'.format(actiondata['name']))
                self.action_name = actiondata['name']
            if 'selected_options' in actiondata.keys():
                print('action_selectedopttion is {}'.format(actiondata['selected_options']))
                seloptlist = actiondata['selected_options']
                for i in range(len(seloptlist)):
                    seloptitem = seloptlist[i]
                    print  ('action_value is {}'.format(seloptitem['value']))
                    self.action_value=seloptitem['value']

        print(data['team'])
        teamdata =  data['team']
        self.team_domain=teamdata['domain']
        self.team_id=teamdata['id']

        print(data['channel'])
        channeldata = data['channel']
        self.channel_name=channeldata['name']
        self.channel_id=channeldata['id']


        print(data['user'])
        userdata = data['user']
        self.user_name=userdata['name']
        self.user_id=userdata['id']

        print(data['attachment_id'])
        self.attachment_id = data['attachment_id']

        print(data['response_url'])
        self.response_url = data['response_url']

        print(data['trigger_id'])
        self.trigger_id = data['trigger_id']

        print(data['is_app_unfurl'])
        self.is_app_unfurl = data['is_app_unfurl']

        print(data['token'])
        self.token = data['token']

        print (data['message_ts'])
        self.message_ts = data['message_ts']

        print (data['action_ts'])
        self.action_ts = data['action_ts']

        print (data['callback_id'])
        self.callback_id = data['callback_id']



# calling point for slack commands
@app.route('/techsched/api/v1.0/commands', methods=['POST'])
def ack_slack_command():

    # assign all vartiables at None
    print('Entered the ack slack command')

    new_command = slack_slash_command(request)

    # start a non blocking thread and call the process_slack_command
    if new_command.command == '/testing':
        _thread.start_new_thread(process_slack_command, ("Thread-1", new_command))
    # repond with a 200
    return ('Hi '+new_command.user_name+', hold on :coffee: is brewing and will be served shortly',202)


# process the command based on the action and command
def process_slack_command(threadName,command):

    print('entered the process slack command')
    response_url = command.response_url
    # doing a wait
    time.sleep(2)
    # check what response needs to be build - depending on the action we serve a response back to slack

    if command.command == '/testing':
        # show option displays the three buttons required.
        print( threadName)
        print("Entered the response builder for a command")
        payload = {
            "text": "What would you like to do?",
            "response_type": "ephemeral",
            "attachments": [
                {
                    "text": "Choose an option",
                    "fallback": "You are unable to choose",
                    "callback_id": "testing_response",
                    "color": "#3AA3E3",
                    "attachment_type": "default",

                    "actions": [
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Testing_Btn_Options",
                            "text": "Check Tech Schedules",
                            "type": "button",
                            "value": "cts"

                        },
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Testing_Btn_Options",
                            "text": "Create a Schedule",
                            "type": "button",
                            "value": "cas"
                        },
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Testing_Btn_Options",
                            "text": "Cancel",
                            "style": "danger",
                            "type": "button",
                            "value": "cancel",
                            "confirm": {
                                "title": "Confirmation",
                                "text": "Are you sure?",
                                "ok_text": "Yes",
                                "dismiss_text": "No"
                            }
                        }
                    ]
                }
            ]
        }
        r =  requests.post(response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})



def process_slack_command_response(threadName,slack_slash_response_command):

    print("Entered the response builder for an action")

    if slack_slash_response_command.callback_id == 'testing_response' and slack_slash_response_command.action_value == 'cts':
        print(threadName)

        payload = {
                    "text": "Schedule a Technician",
                    "response_type": "in_channel",
                    "attachments": [
                        {
                            "text": "Whose Schedule would you need to check ?",
                            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                            "color": "#3AA3E3",
                            "attachment_type": "default",
                            "callback_id": "tech_selection",
                            "actions": [
                                {
                                    "name": "tech_list",
                                    "text": "Choose a Tech...",
                                    "type": "select",
                                    "options": [
                                        {
                                            "text": "Shiyadh",
                                            "value": "shiyadh"
                                        },
                                        {
                                            "text": "Taslim",
                                            "value": "taslim"
                                        },
                                        {
                                            "text": "Vineesh",
                                            "value": "vineesh"
                                        },
                                        {
                                            "text": "Shihab",
                                            "value": "shihab"
                                        },
                                        {
                                            "text": "Subaneesh",
                                            "value": "subaneesh"
                                        },
                                        {
                                            "text": "None",
                                            "value": "cancel"
                                        },
                                        {
                                            "text": "Others",
                                            "value": "others"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
        r = requests.post(slack_slash_response_command.response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})

    elif slack_slash_response_command.callback_id == 'tech_selection' and slack_slash_response_command.action_value == 'others':
        print(threadName)
        print("Entered the response builder")
        payload = {
                    "text": "You need more than a Tech",
                    "response_type": "in_channel",
                    "attachments": [
                        {
                            "text": "Who will that be ?",
                            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                            "color": "#3AA3E3",
                            "attachment_type": "default",
                            "callback_id": "user_selection",
                            "actions": [
                                {
                                    "name": "tech_list",
                                    "text": "Choose a Tech...",
                                    "type": "select",
                                    "data_source": "users"

                                }
                            ]
                        }
                    ]
                }
        r = requests.post(slack_slash_response_command.response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})

    elif slack_slash_response_command.callback_id == 'testing_response' and slack_slash_response_command.action_name == 'cas':
        print(threadName)
        print("Entered the response builder")
        payload = {
                    "text": "You need to check outside ",
                    "response_type": "in_channel",
                    "attachments": [
                        {
                            "text": "What will that be ?",
                            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                            "color": "#3AA3E3",
                            "attachment_type": "default",
                            "callback_id": "extdata_selection",
                            "actions": [
                                        {
                                            "name": "bugs_list",
                                            "text": "Which random bug do you want to resolve?",
                                            "type": "select",
                                            "data_source": "external",
                                            "min_query_length": 3,
                                        }
                                        ]
                        }
                    ]
                }
        r = requests.post(slack_slash_response_command.response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})


@app.route('/techsched/api/v1.0/commands/response', methods=['POST'])

def command_response_parse():

    new_response = slack_slash_response_command(request)


    if new_response.action_value in ['shiyadh','shihab','taslim','vineesh','subaneesh']:
        return 'Hi ' + new_response.user_name + ', You selected ' + new_response.action_value, 200
    elif new_response.action_value in ['cancel']:
        return 'Hi ' + new_response.user_name + ', Have a good day', 200
    elif new_response.action_value in ['others']:
        _thread.start_new_thread(process_slack_command_response, ("Thread-3",new_response))
        return 'Hi ' + new_response.user_name + ', You selected ' + new_response.action_value, 200
    elif new_response.action_value in ['cts']:
        _thread.start_new_thread(process_slack_command_response, ("Thread-4", new_response))
        return 'Hi ' + new_response.user_name + ', We are preparing your data', 200
    else:
        _thread.start_new_thread(process_slack_command_response, ("Thread-2", new_response))
        return 'Hi ' + new_response.user_name + ', You selected ' + new_response.action_value, 200




@app.route('/techsched/api/v1.0/commands/loadextdata', methods=['POST'])
def loadextdata():
    print ("Entered external data")
    keeys = list(request.form.keys())
    valluees = list(request.form.values())
    # printing the json for log purposes
    for i in range(len(keeys)):
        print(keeys[i] + " : " + valluees[i])

    returnjson = [
        {
            "text": "Unexpected sentience",
            "value": "AI-2323"
        },
        {
            "text": "Bot biased toward other bots",
            "value": "SUPPORT-42"
        },
        {
            "text": "Bot broke my toaster",
            "value": "IOT-75"
        }
    ]

    return jsonify({'options': returnjson})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




def main():
    return "Welcome!"


if __name__=="__main__":
    app.run()