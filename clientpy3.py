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


frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
main.bind('<Up>', upKey)
main.bind('<Down>', downKey)
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

def target(our_x, our_y, our_dx, our_dy, x, y):
    direction_to_face = [x - our_x, y - our_y]
    current_velocity = [our_dx, our_dy]


    norm = math.sqrt(direction_to_face[0] ** 2 + direction_to_face[1] ** 2)
    if norm == 0 :
        return

    d_norm = [x/norm for x in direction_to_face]
    v_norm_factor = math.sqrt(current_velocity[0]**2 + current_velocity[1] ** 2)
    if v_norm_factor == 0:
        return

    v_norm = [x/v_norm_factor for x in current_velocity]

    accel_vector = [(3 * v_norm[0]) - (3 * d_norm[0]), (3 * v_norm[1]) - (3 * d_norm[1])]
    if accel_vector[0] == 0:
        return

    angle = - math.atan(accel_vector[1] / accel_vector[0])

    move(angle)

    status()


def status():
    return run(USER, PASSWORD, "STATUS")

def brake():
    run(USER, PASSWORD, "BRAKE")

def scan(x, y):
    run(USER, PASSWORD, "SCAN " + str(x) + " " + str(y))

def set_bomb(x, y, t):
    run(USER, PASSWORD, "BOMB " + str(x) + " " + str(y) + " " + str(t))

def fast_bomb(x, y):
    set_bomb(x, y, 1)

def bomb_mine(our_x, our_y, our_dx, our_dy, x, y):
    if math.fabs(our_x - x) < 100 and math.fabs(our_y - y) < 100:
        set_bomb(our_x, our_y, 300000)
    else
        target(our_x, our_y, our_dx, our_dy, x, y)

def escape(our_x, our_y, our_dx, our_dy):
    if our_dx != 0 and our_dy != 0:
        set_bomb(our_x-1, our_y-1, 5000)
    else
        move (1)
        set_bomb(our_x-1, our_y-1, 5000)

def defend_mine(our_x, our_y, our_dx, our_dy, our_mine_x, our_mine_y):
    if math.fabs(our_x - x) < 500 and math.fabs(our_y - y) < 500:
        escape(our_x, our_y, our_dx, our_dy)
    else
        return

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

        our_coord = our_coord[space + 1:]
        space = our_coord.find(" ")

        our_dx = float(our_coord[:space])

        our_coord = our_coord[space + 1:]
        space = our_coord.find(" ")

        our_dy = float(our_coord[:space])

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

            mine = [coord_x, coord_y]

            if mine not in mines:
                mines.append(mine)

            print(mines)
            target(our_x_coord, our_y_coord, our_dx, our_dy, coord_x, coord_y)
        elif mines:
            sleep(1)
            coords = mines[-1]
            target(our_x_coord, our_y_coord, our_dx, our_dy, coords[0], coords[1])

move(3.14/3)

main.mainloop()

while(True):
    sleep(0.01)
    status()
