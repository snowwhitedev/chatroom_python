import socket, threading
import sys

#thread for client accept
def accept_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        hello = "Hello 1.0"
        cli_sock.send(hello.encode('utf-8'))
        
        #client user name
        uname = cli_sock.recv(1024)
        if not uname:
            error = "Error"
            cli_sock.send(error.encode("utf-8"))
        else:
            name_str = uname.decode("utf-8").strip()
            if name_str[:4] != "NICK" or len(name_str) < 5:
                notification = "Error: Malformed Name"
                cli_sock.send(notification.encode('utf-8'))
            else:
                ok = "OK"
                cli_sock.send(ok.encode('utf-8'))
                #add client
                name_str = uname.decode("utf-8").strip()
                name_str = name_str[4:].strip()
                uname = name_str.encode("utf-8")
                CONNECTION_LIST.append((uname, cli_sock))
                print('%s is now connected' %uname.decode('utf-8'))
                thread_client = threading.Thread(target = broadcast_usr, args=[uname, cli_sock])
                thread_client.start()
            
#thread for sending message
def broadcast_usr(uname, cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
                print (uname.decode('utf-8') + " spoke")
                b_usr(cli_sock, uname, data)
        except Exception as x:
            useless = "end"
            
# send msg to client
def b_usr(cs_sock, sen_name, msg):
    msg_str = msg.decode('utf-8')
    
    for client in CONNECTION_LIST:
        if client[1] != cs_sock:
            if msg_str[:3] == "MSG":
                msg_str = msg_str[3:].strip()
                name_str = sen_name.decode("utf-8")
                send_str = "MSG " + name_str + " " + msg_str 
                client[1].send(send_str.encode('utf-8'))
            else:
                send_str = "MSG " + sen_name.decode("utf-8") + "Error:Malformed Message"

if __name__ == "__main__":
    #get ip port from input arguments  
    if(len(sys.argv) < 2) :
        print ('Usage : python server.py hostname port')
        sys.exit()
    
    HOSTANDPORT = sys.argv[1].strip()
    del_id = HOSTANDPORT.find(":")
    HOST = HOSTANDPORT[:del_id].strip()
    PORT = int(HOSTANDPORT[del_id+1:].strip())
    
    CONNECTION_LIST = []

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind
    ser_sock.bind((HOST, PORT))
    # listen    
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    #thread for client sockets
    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()