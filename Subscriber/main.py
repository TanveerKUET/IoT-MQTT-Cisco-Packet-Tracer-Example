import mqttclient
from time import *
from gpio import *

broker_add ='192.168.0.3'						#Broker Address
username= 'tanveer'								#Username
password = 'g202417180'								#Password
topic = 'switch1'									#Subscription topic
topic2 = 'potentiometer'


def on_connect(status, msg, packet):			#show connection status
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
def on_disconnect(status, msg, packet):			#show disconnection status
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	

def on_subscribe(status, msg, packet):			#show subscription status
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	

def on_unsubscribe(status, msg, packet):		#show unsubscription status
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	

def on_publish(status, msg, packet):			#show publishing status
	if status == "Success" or status == "Error":
		print status + ": " + msg
	elif status == "":
		print msg
	
def on_message_received(status, msg, packet):  #Invoked when new message received
	
	SwStatus = ""
	BrightNess = ""
	
	if packet['topic'] == "switch1":
		
		if packet['payload'] == "0":
			digitalWrite(0,packet['payload'])
			SwStatus = "OFF"
			
		if packet['payload'] == '1023':
			digitalWrite(0,packet['payload'])
			SwStatus = "ON"
			
	
	if packet['topic'] == "potentiometer":
		analogReadval = int(packet['payload'])
		if analogReadval <=350:
			BrightNess = "LOW"
			analogWrite(1, analogReadval)
		if analogReadval >350 and analogReadval <= 700:
			BrightNess = "MID"
			analogWrite(1, analogReadval)
		if analogReadval >700 and analogReadval <= 1023:
			BrightNess = "HIGH"
			analogWrite(1, analogReadval)

	
	LCDMSG="LED: "+" "+SwStatus+"\n"+"DIM LED: "+BrightNess
	customWrite(3, LCDMSG)
	# check received message and take action
	if status == "Success" or status == "Error":
		print status + ": " + msg
	
	elif status == "":
		print msg
	
def main():
	
	mqttclient.init()

	mqttclient.onConnect(on_connect)
	mqttclient.onDisconnect(on_disconnect)
	mqttclient.onSubscribe(on_subscribe)
	mqttclient.onUnsubscribe(on_unsubscribe)
	mqttclient.onPublish(on_publish)
	mqttclient.onMessageReceived(on_message_received)
	print('Client Initialized')

	mqttclient.connect(broker_add,username,password)
	while not mqttclient.state()["connected"]:		#wait until connected
 		pass											#do nothing
 
	mqttclient.subscribe(topic)
	mqttclient.subscribe(topic2)

	while True:
		delay(1000);
		
if __name__ == "__main__":
	main()