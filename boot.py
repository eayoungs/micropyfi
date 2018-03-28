# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import webrepl


gc.collect()

def do_connect():
    from network import WLAN
    wlan = WLAN()
    sta_if = wlan(network.STA_IF)
    # wlan.ifconfig(config=('192.168.0.111', '255.255.255.0', '192.168.0.1',
    #                  '8.8.8.8'))
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssid', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
webrepl.start()
