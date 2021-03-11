import socket               # Import socket module
import time


def TcpSender(host,path):
    start = time.time()
    s = socket.socket()         # Create a socket object
    host = host  #socket.gethostname() # Get local machine name
    port = 12345                 # Reserve a port for your service.
    print(host,path)
    s.connect((host, port))
    f = open(path,'rb')
    print ('Sending...')
    l = f.read(1000)
    count = 0
    while (l):
        print ('Sending...')
        s.send(l)
        l = f.read(1000)
        count = count + 1

    f.close()
    print(f.name)
    print ("Done Sending")
    end = time.time()
    k = str(end - start)[:3]
    s.shutdown(socket.SHUT_WR)
    s.close()
    print("It took " + k + " seconds to send the file @", int(count * 1000.0 / float(k)), "bits per second with", count,
          "packets.")

# TcpSender('192.168.43.134','1.jpg')