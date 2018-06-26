import machine
import socket
import ujson
from umqtt.simple import MQTTClient
# https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_pub.py


pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
adc = machine.ADC(0)

client = MQTTClient('umqtt_client', 'localhost')
client.connect()

while True:
    response_dict = dict([(str(p), p.value()) for p in pins])
    response_dict['ADC(0)'] = adc.read()
    json_response = ujson.dumps(response_dict)

    client.publish(b"topic", "Hello MQTT!")# json_response)

client.disconnect()
