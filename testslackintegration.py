from flask import Flask , jsonify, abort, make_response, request
from flask import render_template
import requests
import json
import _thread
import time


app= Flask(__name__)

class command_summary:
    instance_command = 'empty'

    def __init__(self, command):
        self.instance_command = command


@app.route('/techsched/api/v1.0/commands', methods=['POST'])
def parse_command():

    # assign all vartiables at None
    cursor = 0
    token = None
    team_id = None
    team_domain = None
    channel_id = None
    channel_name = None
    user_id = None
    user_name = None
    command = None
    text = None
    response_url = None
    trigger_id = None

    #obtain the json passed
    keeys = list(request.form.keys())
    valluees = list(request.form.values())
    # printing the json for log purposes
    for i in range(len(keeys)):
        print(keeys[i] + " : " + valluees[i])

    # checking existence of data and assigning the value
    if 'token' in keeys:
        cursor = keeys.index('token')
        token = valluees[cursor]

    if 'team_id' in keeys:
        cursor = keeys.index('team_id')
        team_id = valluees[cursor]

    if 'team_domain' in keeys:
        cursor = keeys.index('team_domain')
        team_domain = valluees[cursor]

    if 'channel_id' in keeys:
        cursor = keeys.index('channel_id')
        channel_id = valluees[cursor]

    if 'channel_name' in keeys:
        cursor = keeys.index('channel_name')
        channel_name = valluees[cursor]

    if 'user_id' in keeys:
        cursor = keeys.index('user_id')
        user_id = valluees[cursor]

    if 'user_name' in keeys:
        cursor = keeys.index('user_name')
        user_name = valluees[cursor]

    if 'command' in keeys:
        cursor = keeys.index('command')
        command = valluees[cursor]

    if 'text' in keeys:
        cursor = keeys.index('text')
        text = valluees[cursor]

    if 'response_url' in keeys:
        cursor = keeys.index('response_url')
        response_url = valluees[cursor]

    if 'trigger_id' in keeys:
        cursor = keeys.index('trigger_id')
        trigger_id = valluees[cursor]

    action = 'show_option'

    _thread.start_new_thread(build_response,("Thread-1",action,command,response_url,))
    return ('Hi '+user_name+', hold on :coffee: is brewing and will be served shortly',202)

def build_response( threadName,action,command,response_url):

    # doing a wait
    time.sleep(2)
    # check what response needs to be build - depending on the action we serve a response back to slack

    if action == 'show_option':
        # show option displays the three buttons required.
        print( threadName)
        print("Entered the response builder")
        payload = {
            "text": "What would you like to do?",
            "response_type": "ephemeral",
            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
            "attachments": [
                {
                    "text": "Choose an option",
                    "fallback": "You are unable to choose",
                    "callback_id": "option_response",
                    "color": "#3AA3E3",
                    "attachment_type": "default",

                    "actions": [
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Option_Response",
                            "text": "Check Tech Schedules",
                            "type": "button",
                            "value": "cts"

                        },
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Option_Response",
                            "text": "Create a Schedule",
                            "type": "button",
                            "value": "cas"
                        },
                        {
                            "response_url": "http://117bc8dd.ngrok.io/techsched/api/v1.0/commands/response",
                            "name": "Option_Response",
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

    elif action == 'show_menu':
        print(threadName)
        print("Entered the response builder")
        payload = {
                    "text": "Would you need help with Tech Schedules?",
                    "response_type": "in_channel",
                    "attachments": [
                        {
                            "text": "Choose a tech",
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
        r = requests.post(response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})

    elif action == 'show_users':
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
        r = requests.post(response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})

    elif action == 'show_extmenu':
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
        r = requests.post(response_url, data=json.dumps(payload))

        print(r.status_code, r.reason)  # return jsonify ({'tasks':tasks})

@app.route('/techsched/api/v1.0/commands/response', methods=['POST'])
def command_response_parse():
    print("Entered response side")
    keeys = list(request.form.keys())
    valluees = list(request.form.values())
    # printing the json for log purposes
    print(len(keeys))
    for i in range (len(keeys)):
        print(keeys[i] + " contains " + valluees[i])

    workablejson = valluees[0]
    data = json.loads(workablejson)

    print(data['actions'])
    dataactionlist = list (data['actions'])
    for i in range(len(dataactionlist)):
        actiondata = dataactionlist[i]
        print (actiondata)
        if 'value' in actiondata.keys():
            print(actiondata['value'])
            action_value = actiondata['value']
        if 'selected_options' in actiondata.keys():
            print(actiondata['selected_options'])
            seloptlist = actiondata['selected_options']
            for i in range(len(seloptlist)):
                seloptitem = seloptlist[i]
                print  (seloptitem['value'])
                action_value=seloptitem['value']
                print(action_value)

    print(data['team'])
    teamdata =  data['team']
    print(teamdata['domain'])

    print(data['channel'])
    channeldata = data['channel']
    print (channeldata['name'])

    print(data['user'])
    userdata = data['user']
    print (userdata['name'])
    user_name = userdata['name']

    print(data['attachment_id'])

    print(data['token'])

    print(data['response_url'])
    response_url = data['response_url']



    if action_value in ['shiyadh','shihab','taslim','vineesh','subaneesh']:
        return 'Hi ' + user_name + ', You selected ' + action_value, 200
    elif action_value in ['cancel']:
        return 'Hi ' + user_name + ', Have a good day', 200
    elif action_value in ['others']:
        _thread.start_new_thread(build_response, ("Thread-3", 'show_users', response_url,))
        return 'Hi ' + user_name + ', You selected ' + action_value, 200
    elif action_value in ['cts']:
        _thread.start_new_thread(build_response, ("Thread-4", 'show_extmenu', response_url,))
        return 'Hi ' + user_name + ', We are preparing your data', 200
    else:
        _thread.start_new_thread(build_response, ("Thread-2", 'show_menu', response_url,))
        return 'Hi ' + user_name + ', You selected ' + action_value, 200




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