import socket               # Import socket module
import time

def connectTCP(path):
    start = time.time()
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    print(host)
    port = 12345                 # Reserve a port for your service.
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.r
    count = 0

    while True:
        c, addr = s.accept()     # Establish connection with client.
        print ('Got connection from', addr)
        file_get=True
        print ("Receiving...")
        f = open('{}'.format(path), 'wb')
        l = c.recv(1000)
        while (l):
            print ("Receiving...")
            f.write(l)
            l = c.recv(1000)
            count = count + 1

        f.close()
        print(f.name)
        print(l)
        print ("Done Receiving")
        end = time.time()
        k = str(end - start)[:3]
        s.close()
        print("It took " + k + " seconds to send the file @", int(count * 1000.0 / float(k)), "bits per second with",
              count, "packets.")
        break
