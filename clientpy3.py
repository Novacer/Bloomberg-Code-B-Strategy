import socket
import sys
from time import sleep



def run(user, password, * commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    data = user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            handle_status(rline.strip())
            rline = sfile.readline()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    data = user + " " + password + "\nSUBSCRIBE\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()

USER = "Friends might come"
PASSWORD = "jzqzhang"

def move(angle):
    run(USER, PASSWORD, "ACCELERATE " + str(angle) + " 1")

def target(our_x, our_y, x, y):
    print(str(our_x) + " " + str(our_y))
    print(str(x) + " " + str(y))


def status():
    return run(USER, PASSWORD, "STATUS")

def brake():
    run(USER, PASSWORD, "BRAKE")

def scan(x, y):
    run(USER, PASSWORD, "SCAN " + str(x) + " " + str(y))

def handle_status(status):
    if status[0:10] == "STATUS_OUT":
        space = status.find(" ")
        our_coord = status[space + 1:]
        space = our_coord.find(" ")

        x_coord = our_coord[:space]
        our_x_coord = float(x_coord)
        our_coord = our_coord[space + 1:]
        space = our_coord.find(" ")
        our_y_coord = float(our_coord[:space])

        index = status.find("MINES")
        if int(status[index+6:index+7]) > 0:
            relevant_status = status[index+8:]
            coord_index = relevant_status.find(" ")
            relevant_status = relevant_status[coord_index + 1:]
            coord_end = relevant_status.find(" ")

            coord_x = float(relevant_status[:coord_end])

            relevant_status = relevant_status[coord_end + 1:]
            coord_end = relevant_status.find(" ")

            coord_y = float(relevant_status[:coord_end])

            target(our_x_coord, our_y_coord, coord_x, coord_y)




move(3.14/6)

while(True):
    sleep(1)
    status()