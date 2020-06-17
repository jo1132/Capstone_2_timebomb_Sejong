import socket
import threading
import time
HOST = '192.168.1.3'    #IP Address
PORT = 12345
A_cro = "0"
B_cro = "0"
C_cro = "0"
D_cro = "0"

A_Lcar = "0"
B_Lcar = "0"
C_Lcar = "0"
D_Lcar = "0"

A_Carnum = "0"
B_Carnum = "0"
C_Carnum = "0"
D_Carnum = "0"

def client_binder(client_socket, addr):
    print('(client)Connected by', addr)
    try :
        while True:
            global A_cro, B_cro, C_cro, D_cro
            global A_Lcar, B_Lcar, C_Lcar, D_Lcar
            global A_Carnum, B_Carnum, C_Carnum, D_Carnum
            msg = A_cro + B_cro + C_cro + D_cro + A_Lcar + B_Lcar + C_Lcar + D_Lcar + A_Carnum + B_Carnum + C_Carnum + D_Carnum
            print(msg)
            data = msg.encode()
            length = len(data)
            client_socket.sendall(length.to_bytes(4, byteorder='big'))
            client_socket.sendall(data)
            time.sleep(0.1)
    except:
            print("except : ", addr)
    finally :
            client_socket.close()

def A_binder(client_socket, addr):
    print('(A_PI)Connected by', addr)
    global A_cro
    global A_Lcar
    global A_Carnum
    try :
        while True:
            msg = client_socket.recv(4)
            msg_dec = msg.decode()
            A_cro = msg_dec[0]
            A_Lcar= msg_dec[1]
            A_Carnum=msg_dec[2]
    except Exception as e:
            print(e)
    finally :
            client_socket.close()



def B_binder(client_socket, addr):
    print('(B_PI)Connected by', addr)
    global B_cro
    global B_Lcar
    global B_Carnum
    try :
        while True:
            msg = client_socket.recv(4)
            msg_dec = msg.decode()
            B_cro = msg_dec[0]
            B_Lcar= msg_dec[1]
            B_Carnum=msg_dec[2]
    except Exception as e:
            print(e)
    finally :
            client_socket.close()



def C_binder(client_socket, addr):
    print('(C_PI)Connected by', addr)
    global C_cro
    global C_Lcar
    global C_Carnum
    try :
        while True:
            msg = client_socket.recv(4)
            msg_dec = msg.decode()
            C_cro = msg_dec[0]
            C_Lcar= msg_dec[1]
            C_Carnum=msg_dec[2]
            print("aaa:%s%s%s"%(C_cro,C_Lcar,C_Carnum))
    except Exception as e:
            print(e)
    finally :
            client_socket.close()

def D_binder(client_socket, addr):
    print('(D_PI)Connected by', addr)
    global D_cro
    global D_Lcar
    global D_Carnum
    try :
        while True:
            msg = client_socket.recv(4)
            msg_dec = msg.decode()
            D_cro = msg_dec[0]
            D_Lcar= msg_dec[1]
            D_Carnum=msg_dec[2]
    except Exception as e:
            print(e)
    finally :
            client_socket.close()




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

try:
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(4)
        length = int.from_bytes(data, "big")
        data = client_socket.recv(length)
        msg = data.decode()
        print('waiting')
        if msg == 'A_pi':
            print('A_pi conected')
            th0 = threading.Thread(target=A_binder, args = (client_socket, addr))
            th0.start()

        elif msg == 'B_pi':            
            print('B_pi conected')
            th1 = threading.Thread(target=B_binder, args = (client_socket, addr))
            th1.start()
        elif msg == 'C_pi':            
            print('C_pi conected')
            th2 = threading.Thread(target=C_binder, args = (client_socket, addr))
            th2.start()
        elif msg == 'D_pi':            
            print('A_pi conected')
            th3 = threading.Thread(target=D_binder, args = (client_socket, addr))
            th3.start()
        elif msg == 'client':            
            print('client conected')
            th4 = threading.Thread(target =  client_binder, args = (client_socket, addr))
            th4.start()

except:
    print("server")
finally:
    server_socket.close()
