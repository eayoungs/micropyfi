import machine
import socket
import json


mpy_pins = (0, 2, 4, 5, 12, 13, 14, 15)
nmcu_keys = ('D3', 'D4', 'D2', 'D1', 'D6', 'D7', 'D5', 'D8')
pins = [machine.Pin(i, machine.Pin.IN) for i in mpy_pins]
adc = machine.ADC(0)

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    response_dict = {str(p): p.value() for p in pins}
    response_dict['ADC(0)'] = adc.read()
    json_response = json.loads(response_dict).encode('utf-8') 

    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    rows.append('<tr><td>%s</td><td>%d</td></tr>' % ('ADC(0)', adc.read()))
    html_response = html % '\n'.join(rows)
 
    cl.send(json_response)
    cl.close()
