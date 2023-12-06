from binascii import hexlify
from bluetooth import BLE
from micropython import const
from time import localtime, sleep

from xiaomi_ble_adv_parse import parse_adv_data,pvxx_pars,atc_pars


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)



def log(*args):
    y, mo, d, h, mi, s, wkd, yd = localtime()
    print("[{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}]".format(y, mo, d, h, mi, s), *args)


def handle_scan(ev, data):
    if ev == _IRQ_SCAN_RESULT:
        addr = hexlify(data[1], ":").decode()
        rssi = data[3]
        parsed = parse_adv_data(data[4])
        if("a4:c1:38:07:11:e6"==addr):
            print(addr,list(data[4]))
            pvxx_data=data[4][3:]
            #pvxx=bytes(list(data[4]))[3:]
            pvxx_pars(pvxx_data)
        else:
            print(addr,list(data[4]))#pvxx olmayan
            atc_data=data[4]
            atc_pars(atc_data)
#         if parsed is None:
#             log("Ignoring {0} (RSSI {1}), doesn't look like a Xiaomi sensor.".format(addr, rssi), parsed)
#         else:
#             log("Device {0} (RSSI {1}):".format(addr, rssi), parsed)
    elif ev == _IRQ_SCAN_DONE:
        log("Scan done.")
    else:
        log("Unexpected event: {0}".format(ev))

#a4:c1:38:07:11:e6
BLE().active(True)
BLE().irq(handle_scan)
log("Starting passive scan. Detection can take seconds or even minutes.")
BLE().gap_scan(20000, 55_000, 25_250)  # scan often & indefinitely
sleep(20)
BLE().active(False)
# You could add your own code here, the scanning runs in the background.
# We explicitly do nothing, simply to prevent the script from ending.
# while True:
#     sleep(5)