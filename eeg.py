print("test")


#poorSignal:0
#EEGPower:1

import csv
import thinkgear
import datetime
import os
import sys

def to_dec(text):
    tex2 = str(text).split('(')
    tex3 = tex2[1].split(',')

    eeg = {}

    for i in range(len(tex3)):
        data = tex3[i].split('=')
        eeg[data[0].replace(' ', '')] = int(str(data[1].replace(')', '')))
    
    return eeg


PORT = 'COM5'

count = 0
preMsec = -1

start = datetime.datetime.now()
file_path = "thinkgear_data/%d_%d_%d_%d" %(start.month, start.day, start.hour, start.minute)

file_name = "%d_%d_%d_%d_raw.csv" %(start.month, start.day, start.hour, start.minute)
file_name2 = "%d_%d_%d_%d_spec.csv" %(start.month, start.day, start.hour, start.minute)

os.mkdir(file_path)

with open(file_path + '/' + file_name, 'w') as f:
    writer = csv.writer(f,delimiter=',',lineterminator="\n")
    writer.writerow(["hour", "minute", "second", "msec", "raw"])

with open(file_path + '/' + file_name2, 'w') as f:
    writer = csv.writer(f,delimiter=',',lineterminator="\n")
    writer.writerow(["hour", "minute", "second", "msec", "alphaLow", "alphaHigh", "betaLow", "betaHigh", "gammmaLow", "gammmaMid", "delta", "theta", "signal"])


try:
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        second = time.second
        msec = time.microsecond
        count += 1
        #print(count)

        if isinstance(packets[0], thinkgear.ThinkGearRawWaveData):
            #rawdata
            data_raw = int(str(packets[0]))
            if msec != preMsec:
                with open(file_path + '/' + file_name, 'a') as f:
                    writer = csv.writer(f,delimiter=',',lineterminator="\n")
                    writer.writerow([hour, minute, second, msec, data_raw])
        else:
            #spectrum
            signal = 100 - int(str(packets[0]))
            print("\nsignal level : " + str(signal) + "\n")
            
            spec = to_dec(packets[1])
            print(spec)
            with open(file_path + '/' + file_name2, 'a') as f:
                writer = csv.writer(f,delimiter=',',lineterminator="\n")
                writer.writerow([hour, minute, second, msec, spec["lowalpha"], spec["highalpha"], spec["lowbeta"], spec["highbeta"], spec["lowgamma"], spec["midgamma"], spec["delta"], spec["theta"], signal])

        preMsec = msec
except KeyboardInterrupt:
    print("\nfinish")
    sys.exit(0)
except:
    print("error occured.")
