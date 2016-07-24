from .utils import get_pokemon_name
from pogom.utils import get_args
from datetime import datetime

import httplib
import urllib
import json

args = get_args()

ignore = []
if args.ignore:
    ignore = [i.lower().strip() for i in args.ignore.split(',')]
alreadyseen = {}
              
def outputToSlack(id,encounter_id,lat,lng,itime):
    slack_webhook_urlpath = str(args.slack_webhook)
    pokemon_name = get_pokemon_name(id)
    if args.ignore:
        if pokemon_name.lower() in ignore or id in ignore:
            return

    if encounter_id in alreadyseen.keys():
        return
            
    if args.pokemon_icons != ':pokeball:':
        user_icon = args.pokemon_icons + pokemon_name.lower() + ':'
    else:
        user_icon = ':pokeball:'

    time_till_disappears = itime - datetime.now()
    disappear_hours, disappear_remainder = divmod(time_till_disappears.seconds, 3600)
    disappear_minutes, disappear_seconds = divmod(disappear_remainder, 60)
    disappear_minutes = str(disappear_minutes)
    disappear_seconds = str(disappear_seconds)
    if len(disappear_seconds) == 1:
        disappear_seconds = str(0) + disappear_seconds
    disappear_time = itime.strftime("%H:%M:%S")
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng)
    response = urllib.urlopen(url)
    loc_dic = json.loads(response.read())
    print loc_dic['results'][0]['address_components'][1]['long_name']
    text = "You can find me at <http://maps.google.com/maps?q=loc:" + str(lat) + "," + str(lng) + \
            "| " + loc_dic['results'][0]['address_components'][1]['long_name'] + \
            " " + loc_dic['results'][0]['address_components'][0]['long_name'] + "> until " + disappear_time + \
            " (" + disappear_minutes + ":" + disappear_seconds + ")!"
    data = urllib.urlencode({'payload': '{"username": "' + pokemon_name + '", '
                                        '"icon_emoji": "' + user_icon + '", '
                                        '"text": "' + text + '"}'
                             })

    h = httplib.HTTPSConnection('hooks.slack.com')
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    h.request('POST', slack_webhook_urlpath, data, headers)
    r = h.getresponse()
    ack = r.read()
    
    alreadyseen[encounter_id] = pokemon_name
    
    
    
    
    #global slack_webhook_urlpath
    #slack_webhook_urlpath = str(args.slack_webhook)

    #global pokemon_icons_prefix
    #if args.pokemon_icons:
    #    pokemon_icons_prefix = args.pokemon_icons
    #else:
    #    pokemon_icons_prefix = False