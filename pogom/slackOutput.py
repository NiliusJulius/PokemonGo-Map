from .utils import get_pokemon_name
from pogom.utils import get_args
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt, atan2, degrees

#import httplib
#import urllib
import json
import logging
import requests
from pokedata import Pokedata

logger = logging.getLogger(__name__)

args = get_args()

ignore = []
if args.ignore:
    ignore = [i.lower().strip() for i in args.ignore.split(',')]
 
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
	
def calculate_initial_compass_bearing(latd1, lond1, latd2, lond2):

    lat1 = radians(latd1)
    lat2 = radians(latd2)

    diffLong = radians(lond1 - lond2)

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180 to + 180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
 
def outputToSlack(id,encounter_id, enc_ids, lat,lng,itime):

    if itime < datetime.utcnow():
        return
        
    pokedata = Pokedata.get(id)
    if pokedata['rarity'] <= args.rarity_limit:
        logger.info('Rarity not high enough')
        return

    slack_webhook_urlpath = str(args.slack_webhook)
    pokemon_name = get_pokemon_name(id)
    if args.ignore:
        if pokemon_name.lower() in ignore or id in ignore:
            return

    #print encounter_id
    #print enc_ids
    if encounter_id in enc_ids.keys():
        logger.info('already sent this pokemon to slack')
        return
            
    if args.pokemon_icons != ':pokeball:':
        user_icon = args.pokemon_icons + pokemon_name.lower() + ':'
    else:
        user_icon = ':pokeball:'
    
    loc = [l.strip() for l in args.location.split(',')]
    distance = lonlat_to_meters(float(loc[0]), float(loc[1]), lat, lng)
    compass = calculate_initial_compass_bearing(float(loc[0]), float(loc[1]), lat, lng)
    compass_text = ""
    if compass < 90:
        compass_text = "Noord-West"
    elif compass < 180:
        compass_text = "Zuid-West"
    elif compass < 270:
        compass_text = "Zuid-Oost"
    else: compass_text = "Noord-Oost"
    
    time_till_disappears = itime - datetime.utcnow()
    disappear_hours, disappear_remainder = divmod(time_till_disappears.seconds, 3600)
    disappear_minutes, disappear_seconds = divmod(disappear_remainder, 60)
    disappear_minutes = str(disappear_minutes)
    disappear_seconds = str(disappear_seconds)
    if len(disappear_seconds) == 1:
        disappear_seconds = str(0) + disappear_seconds
    disappear_time = itime.strftime("%H:%M:%S")
    #url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng)
    #response = urllib.urlopen(url)
    #loc_dic = json.loads(response.read())
    #print loc_dic
    #print loc_dic['results'][0]['address_components'][1]['long_name']
    text = "<http://maps.google.com/maps?q=loc:" + str(lat) + "," + str(lng) + \
            "|" + '{0:.2f}'.format(distance) + \
            " m> afstand tot basiliek, in richting " + compass_text + ", tot: " + disappear_time + \
            " (" + disappear_minutes + ":" + disappear_seconds + ")!"
            
    payload = {"username": pokemon_name,
              "icon_emoji": user_icon,
              "text": text
    }

    #h = httplib.HTTPSConnection('hooks.slack.com')
    #headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    #h.request('POST', slack_webhook_urlpath, data, headers)
    #r = h.getresponse()
    #ack = r.read()
    
    webhook = "https://hooks.slack.com" + slack_webhook_urlpath
    s = json.dumps(payload)
    r = requests.post(webhook, data=s)
    logger.info('slack post result: %s, %s', r.status_code, r.reason)
    
    
            #"| " + loc_dic['results'][0]['address_components'][1]['long_name'] + \
            #" " + loc_dic['results'][0]['address_components'][0]['long_name'] + "> until " + disappear_time + \