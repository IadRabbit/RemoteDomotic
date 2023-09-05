from time import sleep
from PyP100 import PyP100
from pprint import pprint as pp

#pp(devices)
p100 = PyP100.P100("YOUR_BULB_IP", "YOUR_EMAIL", "YOUR_PASSWORD") #Creating a P100 plug object

#p100.handshake() #Creates the cookies required for further methods 
#p100.login() #Sends credentials to the plug and creates AES Key and IV for further methods

#p100.turnOn() #Sends the turn on request
#p100.setBrightness(50) #Sends the set brightness request
p100.turnOff() #Sends the turn off request
sleep(1)
p100.turnOn()
#p100.setColor(100, 300)
#print(p100.getStatus())
#pp(p100.getDeviceInfo()['result']['hue']) #Returns dict with all the device info