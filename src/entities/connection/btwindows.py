import bluetooth
import time

def receivemessages():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Waiting for connection...")

    client_sock, address = server_sock.accept()
    print("Accepted connection from " + str(address))
    time.sleep(3)

    while True:
        data = client_sock.recv(4096)
        print("Received: %s" % data)
        if data == "q":
            break

    client_sock.close()
    server_sock.close()


def reveiveard():
    bd_addr = "98:D3:31:FD:15:C1" # The address from Boris
    port = 1
    sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
    try:
        sock.connect((bd_addr, port))
        print("Connected!")
    except bluetooth.btcommon.BluetoothError:
        print("No connection possible.")
        return
     
    data = ""
    
    while 1:
        try:
            data += str(sock.recv(1024))[2:][:-1]
            #print(data)
            data_start = data.find('start')
            data_end = data.find('stop')
            
            if data_start != -1:
                next = str(sock.recv(1024))[2:][:-1]
                data_end = next.find('stop')
                while data_end == -1:
                    data += next
                    next = str(sock.recv(1024))[2:][:-1]
                    data_end = next.find('stop')
                data += next[:data_end]
                
                packages = data.split('stop')
                
                for i in range(len(packages)): 
                    handlePackage(packages[i][5:])
                data = next[data_end:]
                    
            
            
            if data_end != -1:
                rec = data[:data_end]
                #print(rec)
                data = ""
        except KeyboardInterrupt:
            break
    sock.close()

def handlePackage(data):
    props = data.split(',')
    for i in range(len(props)):
        print(props[i])

def sendmessageto(target):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target, port))
    sock.send("Dit is ontvangen met bluetooth")
    sock.close()


def looknearby():
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print(str(bluetooth.lookup_name(bdaddr)) + " [" + str(bdaddr) + "]")


reveiveard()
# receivemessages()
# sendmessageto("98:D3:31:FD:15:C1") # Boris CS
# sendmessageto("B8:27:EB:F6:A8:B2") # Pi
# looknearby()
