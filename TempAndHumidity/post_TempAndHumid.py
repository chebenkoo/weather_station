#!/usr/bin/env python

import os
import requests
import json
import paho.mqtt.publish as publish	# Update Channel via MQTT publish messages


# Use Paho MQTT client; three MQTT connection methods exist:
# - conventional TCP socket on port 1882: useUnsecuredTCP=True 
#   (uses the least amount of system ressources) 
# - WebSockets (useful when default MQTT port in blocked on local network, 
#   uses port 80): useUnsecuredWebsockets=True
# - SSL (if encryption is required): useSSLWebsockets=True
useUnsecuredTCP=False
useUnsecuredWebsockets=False
useSSLWebsockets=True

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443


THINGSAPIKEY = "JT89Z7U0GAFWT1SD"
# THINGSAPIKEY = os.environ['THINGSAPIKEY']

CHANNELID = "317758"
MQTTHOST = "mqtt.thingspeak.com"

# -------------------------------------------------------------
# print "\nUpdate a channel via HTTP/REST interface"

#tPayload = {'api_key' : THINGSAPIKEY }
#i = 1
#with os.popen("~/IoT/TempAndHumidity/th02.py") as handle:
#	for line in handle:
#		lineContend = line.split(' ')
#		ind = lineContend.index(":")
#		value = float(lineContend[ind+1])
#		field = "field{0}".format(i)
#		tPayload[field] = value
#		i +=1 
#print tPayload

#r = requests.get('https://api.thingspeak.com/update', data=tPayload)
#if r.status_code !=200:
#	print(r.text)
# -------------------------------------------------------------

print "\nBegin------>"
# Create the topic string (MQTT)
# and attempt to publish data to the topic 
# using the MQTT client
print "\nUpdate a channel via MQTT client:"

topic = "channels/" + CHANNELID + "/publish/" + THINGSAPIKEY
print topic

i = 1
tPayloadMQTT = ""
with os.popen("~/IoT/TempAndHumidity/th02.py") as handle:
	for line in handle:
		if i>1:
			tPayloadMQTT += "&"
		lineContend = line.split(' ')
		ind = lineContend.index(":")
		value = float(lineContend[ind+1])
		field = "field{0}={1}".format(i,value)
		tPayloadMQTT += field
		i +=1 
print tPayloadMQTT

try:
	publish.single(topic, payload=tPayloadMQTT, hostname=MQTTHOST, port=tPort, tls=tTLS, transport=tTransport)
except:
	print("There was an error while publishing the data!")

print "\n------>"

#print "\nGet a channel field:"
#tPayload_get = {'api_key' : 'U2Q7JVN80VQCIOHX', 'results' : '1' }
#r = requests.get('https://api.thingspeak.com/channels/317758/fields/1.json', data=tPayload_get)
#print r.status_code
#print r.text

print "\nGet a channel feed:"
tPayload_get = {'api_key' : 'U2Q7JVN80VQCIOHX', 'results' : '1' }
r = requests.get('https://api.thingspeak.com/channels/317758/feeds.json', data=tPayload_get)
print r.status_code
print r.text
text = json.loads(r.text)
feed = text['feeds'][0]
channel = text['channel']
print "\nattributes--->"
print "Sensor name: %s" % (channel['name'])
print "Creation time: %s" % (feed['created_at'])
print "Entry number: %s" % (feed['entry_id'])
print "Temperature: %s" % (feed['field2'])
print "Humidity: %s" % (feed['field1'])
print "Latitude: %s" % (channel['latitude'])
print "Longitude: %s" % (channel['longitude'])
print "<---attributes"
print "\n------>End"

# r = requests.get('https://api.thingspeak.com/channels/317758/status.json')
# print r.status_code
# print r.text