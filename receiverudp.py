# ----- receiver.py -----

#!/usr/bin/env python
import time
from socket import *
import time


def receiverudp(path):
    start = time.time()
    host=gethostname()
    port = 9999
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((host,port))

    addr = (host,port)
    buf=1000
    count = 1
    data,addr = s.recvfrom(buf)
    f = open(path,'wb')

    data,addr = s.recvfrom(buf)


    try:
        while(data):
            print("Receiving ...")
            f.write(data)
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
            count = count + 1
    except timeout:
        f.close()
        s.close()
        print ("File Downloaded")
        end = time.time()
        k = str(end - start)[:3]
        print("It took " + k + " seconds to download the file @", int(count * 1000.0 / float(k)), "bits per second with", count,"packets.")

