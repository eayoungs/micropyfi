import machine
import socket
import ujson


pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
adc = machine.ADC(0)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

f_name = "pin.log"

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    response_dict = dict([(str(p), p.value()) for p in pins])
    response_dict['ADC(0)'] = adc.read()
    json_response = ujson.dumps(response_dict)
 
    with open(f_name, mode='w', encoding='utf-8') as f:
        f.write(json_response)
        f.write('\n')

    cl.send(json_response)
    cl.close()
