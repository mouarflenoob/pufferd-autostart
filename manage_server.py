#######################################################################################################
#
#   Description: A python script for remote-requests on "PufferPanel" (https://www.pufferpanel.com/)
#   
#   Author Sascha Frank < sfrank@whatsyourlanguage.world >
#   License: --- Free to Use ---
#
#######################################################################################################

import urllib
from urllib.parse import urlparse, parse_qs
import requests
from argparse import ArgumentParser

client_id = 'Rasputin12'                # SampleData
client_secret = '1888inasimpleway123'   # generated secret key via panel

server_ip="95.217.59.142"               
server_port=5656
server_name="mc2.wyl-server.host"

parser = ArgumentParser()
parser.add_argument("-a", "--action", dest="action",
                    help="Start SERVER_ACTION", metavar="SERVER_ACTION") 
parser.add_argument("-n", "--name", dest="name",
                    help="Name of the Server")

parser.add_argument("-s", "--ssl", dest="ssl_enabled",
                    help="Is Panel Secured?")
   
########################################################################################################
   

args = parser.parse_args()


def get_proto():
    if args.ssl_enabled == "1":
        return "https" 
    else:
        return "http"

proto = get_proto();

def auth__oauth2():
    payload_querystr = "grant_type=client_credentials&client_id="+client_id+"&client_secret="+client_secret
    payload = urllib.parse.parse_qs(payload_querystr)
    token = False;
    defaultAuthUrl = get_AuthUrl(server_name)
    r = requests.post(defaultAuthUrl, params=payload)
    if "error" in r.text:
        print("Error: "+r.text)
        exit;
    else:
        token = r.json()['access_token']
    
    return token



def createAuthHeader(token):
    return {'Authorization': 'Bearer '+token}



def get_AuthUrl(server_name):
    
    return proto+"://"+server_name+'/oauth2/token/request'

def gen_DefaultUrl(proto,server_name,server_port,gameserver_name):
    url = proto+"://"+server_name+":"+str(server_port)+"/server/"+gameserver_name+"/"
    return url
    
def generate_ActionURL(token, gameserver_name, action):
    #proto = get_proto();
    defaultReqURL = (gen_DefaultUrl(proto,server_name,server_port,gameserver_name))
    actionReqURL = defaultReqURL+action
    return actionReqURL
    
def manage_server(token, gameserver_name, action):
    headers = createAuthHeader(token)
    actionReqURL = generate_ActionURL(token, gameserver_name, action)
    r = requests.get(actionReqURL, headers=headers)
    print(r.text) 

########################################################################################################

if len(args.action) > 0:
    token = auth__oauth2()
    print(token)
    if token is not False:
        if len(args.name) > 0:
            gameserver_name = args.name
        else:
            gameserver_name = "mc2_test"
            
        if args.action == "start":
            manage_server(token, gameserver_name, "start")
        elif args.action == "stop":
            manage_server(token, gameserver_name, "stop")
