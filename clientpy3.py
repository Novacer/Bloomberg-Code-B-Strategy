import socket
import sys
from time import sleep
import math


from tkinter import *

main = Tk()

def leftKey(event):
    move(3.1415926535)

def rightKey(event):
    move(0)

def upKey(event):
    move(-1.57)

def downKey(event):
    move(1.57)

def space(event):
    brake()


frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind('<Up>', upKey)
main.bind('<Down>', downKey)
main.bind('<space>', space)
frame.pack()

mines = []

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

def ret_run(user, password, * commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    data = user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            return rline.strip()

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

def move_slow(angle):
    run(USER, PASSWORD, "ACCELERATE " + str(angle) + " 0.25")

def target(our_x, our_y, our_dx, our_dy, x, y):
    direction_to_face = [x - our_x, y - our_y]
    current_velocity = [our_dx, our_dy]

    norm = math.sqrt(math.pow(direction_to_face[0], 2) + math.pow(direction_to_face[1], 2))
    if norm == 0:
        return

    d_norm = [x/norm for x in direction_to_face]
    #v_norm_factor = math.sqrt(math.pow(current_velocity[0], 2) + math.pow(current_velocity[1], 2))
    #if v_norm_factor == 0:
     #   return

    #v_norm = [x/v_norm_factor for x in current_velocity]

    #accel_vector = [(v_norm[0]) - (d_norm[0]), (v_norm[1]) - (d_norm[1])]
    #if accel_vector[0] == 0:
     #   return

    angle = - math.atan2(d_norm[1],  d_norm[0])
    print("moved: " + str(angle))
    move(angle)


def status():
    return run(USER, PASSWORD, "STATUS")

def brake():
    run(USER, PASSWORD, "BRAKE")

def scan(x, y):
    run(USER, PASSWORD, "SCAN " + str(x) + " " + str(y))

def set_bomb(x, y, t):
    run(USER, PASSWORD, "BOMB " + str(x) + " " + str(y) + " " + str(t))

def fast_bomb(x, y):
    set_bomb(x, y, 10000)


def handle_status(status):
    if status[0:10] == "STATUS_OUT":
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
            brake()
            sleep(4)
            aim(coord_x, coord_y)
            print("coords: ", coord_x, coord_y)
            mine = [coord_x, coord_y]

            if mine not in mines:
                mines.append(mine)


        elif mines:
            coords = mines[-1]
            aim(coords[0], coords[1])

        else:
            move(3.141592/4)

def aim(x, y):
    m_status = ret_run(USER, PASSWORD, 'STATUS')

    m_space = m_status.find(" ")
    our_coord = m_status[m_space + 1:]
    m_space = our_coord.find(" ")

    x_coord = our_coord[:m_space]
    our_x_coord = float(x_coord)
    our_coord = our_coord[m_space + 1:]
    m_space = our_coord.find(" ")
    our_y_coord = float(our_coord[:m_space])

    our_coord = our_coord[m_space + 1:]
    m_space = our_coord.find(" ")

    our_dx = float(our_coord[:m_space])

    our_coord = our_coord[m_space + 1:]
    m_space = our_coord.find(" ")

    our_dy = float(our_coord[:m_space])

    target(our_x_coord, our_y_coord, our_dx, our_dy, x, y)

move(3.14/3)

main.mainloop()

while(True):
    sleep(0.01)
    status()

