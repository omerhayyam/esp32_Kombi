import network
#from utime import sleep
#ap=network.WLAN(network.AP_IF)
#ap.config(ssid='ESP-AP')
#ap.active(False)
sta=network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('***','***')
#sta.connect('TP-Link_2929','ASDfgh123')
#sleep(3)
#print(sta.ifconfig())

