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
 
	
	
	
	
	while True:
		delay(1000);
		SwStatus = "OFF"
		BrightNess = ""
		
		digitalVal = digitalRead(0)
		if(digitalVal >0):
			SwStatus = "ON"
		mqttclient.publish(topic,str(digitalVal),'1')
		
		analogReadval = analogRead(1)
		
		if analogReadval <=350:
			BrightNess = "LOW"
		if analogReadval >350 and analogReadval <= 700:
			BrightNess = "MID"
		if analogReadval >700 and analogReadval <= 1023:
			BrightNess = "HIGH"
		
		mqttclient.publish(topic2,str(analogReadval),'1')
		
		LCDMSG="LED: "+" "+SwStatus+"\n"+"DIM LED: "+BrightNess
		customWrite(3, LCDMSG)
		
if __name__ == "__main__":
	main()