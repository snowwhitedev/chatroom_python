import socket, threading
import re
import sys

global running
running = True

#thread to send message
def send():
    global running
    while True:
        msg = input()
        if msg == 'exit':
           running = False
           closeChat()
           break
        if len(msg) > 255:
            print("We can send only 255 characters")
            msg = msg[:255]
        msg = "MSG " + msg
        cli_sock.send(msg.encode('utf-8'))

#thread to receive message
def receive():
    while True:
        if running == False:
            break
        try:
            data = cli_sock.recv(1024)
            data_str = data.decode('utf-8').strip()
            if(data_str[:3] != "MSG"):
                print("Malformated Message from host")
            else:
                data_str = data_str[3:].strip()
                index = data_str.find(" ")
                rec_name = data_str[:index].strip()
                rec_msg = data_str[index:].strip()
                print(rec_name + ":" + rec_msg)
        except:
            print("")
        else:
            print("")
#clise chat
def closeChat():
    try:
        cli_sock.close()
    except:
        print("END")
    else:
        print("END")
    sys.exit()

if __name__ == "__main__":   
    if(len(sys.argv) < 3) :
        print ('Usage : python client.py hostname:port name')
        sys.exit()
    
    HOSTANDPORT = sys.argv[1].strip()
    del_id = HOSTANDPORT.find(":")
    HOST = HOSTANDPORT[:del_id].strip()
    PORT = int(HOSTANDPORT[del_id+1:].strip())
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect
    cli_sock.connect((HOST, PORT))
    server_reply = cli_sock.recv(1024)
    print(server_reply.decode("utf-8"))  
    # print('Connected to remote host...')
    
    uname =sys.argv[2].strip()
    if len(uname) > 12:
        print("Nickname is limited to 12 characters. Please Input again.")
        sys.exit()
    else: 
        validChars =  re.findall("[a-zA-Z0-9]", uname)
        if len(validChars) != len(uname):
            print("Nick name chars have to be lower or upper case, or digits. Please Input again")
            sys.exit()
    
    uname = "NICK " + uname + ""
    
    cli_sock.send(uname.encode('utf-8'))
    server_reply = cli_sock.recv(1024)
    print(server_reply.decode("utf-8"))
    
    if server_reply.decode('utf-8').strip() != 'OK':
        sys.exit()
    #start thread
    thread_send = threading.Thread(target = send)
    thread_send.start()
    
    thread_receive = threading.Thread(target = receive)
    thread_receive.start()