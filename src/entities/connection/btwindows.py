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
    
    sock.connect((bd_addr, port))
     
    data = ""
    
    count = 0
    while 1:
        try:
            data += str(sock.recv(1024))[2:][:-1]
            data_end = data.find('\\n')
            if data_end != -1:
                rec = data[:data_end]
                print(rec)
                data = ""
                count += 1
                    
        except KeyboardInterrupt:
            break
    sock.close()
    

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