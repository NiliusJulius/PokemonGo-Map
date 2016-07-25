from .utils import get_pokemon_name
from pogom.utils import get_args
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

import httplib
import urllib
import json

args = get_args()

ignore = []
if args.ignore:
    ignore = [i.lower().strip() for i in args.ignore.split(',')]
alreadyseen = {}
 
def lonlat_to_meters(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # earth radius in meters: 6378100
    m = 6378100 * c
    return m
 
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
    
    loc = [l.strip() for l in args.location.split(',')]
    #print "heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeej" + str(loc[0])
    distance = lonlat_to_meters(float(loc[0]), float(loc[1]), lat, lng)
    print distance
        
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
    #print loc_dic
    #print loc_dic['results'][0]['address_components'][1]['long_name']
    text = "<http://maps.google.com/maps?q=loc:" + str(lat) + "," + str(lng) + \
            "|" + '{0:.2f}'.format(distance) + \
            " m> afstand, tot: " + disappear_time + \
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
    
    
            #"| " + loc_dic['results'][0]['address_components'][1]['long_name'] + \
            #" " + loc_dic['results'][0]['address_components'][0]['long_name'] + "> until " + disappear_time + \