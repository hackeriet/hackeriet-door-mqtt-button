import network
import time
import machine
import ujson
import ubinascii
import sys
from umqtt.robust import MQTTClient



with open('config.json') as fp:
    config = ujson.loads(fp.read())

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(config['wifi']['ssid'],config['wifi']['psk'])

while not station.isconnected():
    machine.idle()

ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
  ap_if.active(False)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

c = MQTTClient(client_id = CLIENT_ID,
               server     = config['mqtt']['server'],
               user       = config['mqtt']['user'],
               password   = config['mqtt']['password'],
               port       = config['mqtt']['port'],
               ssl        = config['mqtt']['ssl']
)


led = machine.Pin(5, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def beep(dur=60):
    led.value(1)
    time.sleep_ms(dur)
    led.value(0)


while True:
    if not button.value():
        c.connect(clean_session = False)
        c.publish("hackeriet/labradoor", "open")
        c.disconnect()

        d = 500
        while d >= 0:
            beep()
            time.sleep_ms(d)
            d = d - 20
        beep(2000)

