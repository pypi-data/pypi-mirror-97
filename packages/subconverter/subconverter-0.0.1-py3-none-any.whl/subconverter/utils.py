def fr_to_ms(fr, frame_rate=24.00):
    return int((fr*1000)/frame_rate)

def ms_to_fr(ms, frame_rate=24.00):
    return int((ms*frame_rate)/1000)
