# ----- sender.py ------

#!/usr/bin/env python

from socket import *
import time


def UdpSender(host,path):
    start=time.time()
    s = socket(AF_INET,SOCK_DGRAM)
    host = host
    port = 9999
    buf =1000
    addr = (host,port)
    count=0
    file_name= bytes(path,'utf-8')
    s.sendto(file_name,addr)
    f=open(file_name,"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            print ("sending ...")
            data = f.read(buf)
            count = count + 1

    end = time.time()
    k = str(end - start)[:3]
    s.close()
    f.close()
    print("It took "+k + " seconds to send the file @", int(count*1000.0/float(k)),"bytes per second with", count,"packets.")

