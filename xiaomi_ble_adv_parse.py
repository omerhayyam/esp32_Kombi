from struct import unpack


def parse_adv_data(adv_data: bytes):
    start = 0
    while start < len(adv_data):
        l = adv_data[start]    # length of element
        if l >= 18:  # the elements we're interested in are at least that long
            t = adv_data[start+1]  # type of element
            if t == 0x16:  # service data
                (uuid,) = unpack("<H", adv_data[start+2:start+4])
                if uuid == 0x181a:  # the type we're interested in
                    (t,) = unpack("<H", adv_data[start+15:start+17])  # value type
                    vl = adv_data[start+17]  # value length
                    if vl <= l - 17:  # make sure we don't overshoot
                        v = adv_data[start+18:start+18+vl]
                        if t == 0x1004 and vl == 2:  # temp
                            (temp,) = unpack("<h", v)
                            return {"t": temp/10}
                        if t == 0x1006 and vl == 2:  # hum
                            (hum,) = unpack("<H", v)
                            return {"h": hum/10}
                        if t == 0x100a and vl == 1:  # battery
                            (bat,) = unpack("<B", v)
                            return {"b": bat}
                        if t == 0x100d and vl == 4:  # temp+hum
                            temp, hum = unpack("<hH", v)
                            return {"t": temp/10, "h": hum/10}
        start += l+1
        
def pvxx_pars(pvxx_data):
    if pvxx_data[0]==18 :
        t = unpack("<H",pvxx_data[10:12])[0]/100#sicaklik 0.01derece
        h = unpack("<H",pvxx_data[12:14])[0]/100#nem      0.01%
        b_mv = unpack("<H",pvxx_data[14:16])[0]#batarya mV
        b_lvl= unpack("<B",pvxx_data[16:17])[0]#batarya %0..100
        c = unpack("<B",pvxx_data[17:18])[0]#olcum adedi
        print("Pvxx sicaklik:",t,"  nem:",h,"   Batarya_mV-%:",b_mv,"mV - %",b_lvl,"   adet:",c)
        
def atc_pars(atc_data):
    if atc_data[0]==18 :
        t = unpack("<H",atc_data[10:12])[0]/100#sicaklik 0.01derece
        h = unpack("<B",atc_data[12:13])[0]#nem      0.01%
        b_lvl = unpack("<B",atc_data[13:14])[0]#batarya %0..100
        b_mv= unpack("<H",atc_data[14:16])[0]#batarya mV
        c = unpack("<B",atc_data[16:17])[0]#olcum adedi
        print("Atc  sicaklik:",t,"  nem:",h,"   Batarya_mV-%:",b_mv,"mV - %",b_lvl,"   adet:",c)
        