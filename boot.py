# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import webrepl


gc.collect()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    # network.WLAN.ifconfig(config=('fixed_ip', '255.255.255.0',
    #                               'router_ip', 'routers_ip'))
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssid', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
webrepl.start()
