# %%
from multiprocessing import Process, Queue
import argparse
import time, sys, os
import ifmO3rViewer.viewer as viewer
from ifmO3r.ifm3dTiny.utils import utils

LIVE = False # start the PCIC server not endlessly running
AMOUNT = 50 # if PCIC server not live, collect 'amount' of images before disconnecting

# %%
def start_viewer(port):
    """
    Calls the viewer. A waiting time is implemented, to ensure that 
    the viewer is started before the server. Processes take a bit time to
    start.
    """
    print("Starting viewer")
    time.sleep(1)
    print("viewer")
    viewer.startGUI(port=port)

def start_server(port, ip):
    """
    Calls the PCIC server. A waiting time is implemented, to ensure that 
    the viewer is started before the server. Processes take a bit time to
    start.

    :live:  True= live mode, endlessly taking images, 
            False= Together with amount, it will take the amount of images
    :amount:    How many images should be taken
    """
    print("Starting server")
    time.sleep(5)
    print("server")
    utils.hostPCICserver(ip, port)

def start_2_heads(ip='192.168.0.69', port1=50012, port2=50013):
    processes = [
        Process(target=start_viewer, args=(port1, )),
        Process(target=start_server_2_heads, args=(ip, port1, port2,))
    ]

    for p in processes:
        p.start()

    for p in processes:
        """ if proccesses are done, wait till other processes are
        also over before closing the program. This might come in handy,
        if logging files are still running.
        """
        p.join()


def start_server_2_heads(ip, port1, port2):
    """
    Calls the PCIC server. A waiting time is implemented, to ensure that
    the viewer is started before the server. Processes take a bit time to
    start.

    :live:  True= live mode, endlessly taking images,
            False= Together with amount, it will take the amount of images
    :amount:    How many images should be taken
    """
    print("Starting server")
    time.sleep(5)
    print("server")
    utils.hostPCICserver_2Heads(ip=ip, port1=port1, port2=port2)

def start(port=50012,ip='192.168.0.69'):
    """
    Add start_viewer and start_server to proccess list and start them.

    :live:  True= live mode, endlessly taking images, 
            False= Together with amount, it will take the amount of images
    :amount:    How many images should be taken
    """
    processes = [
        Process(target=start_viewer, args=(port, )),
        Process(target=start_server, args=(port, ip))
    ]

    for p in processes:
        p.start()

    for p in processes:
        """ if proccesses are done, wait till other processes are
        also over before closing the program. This might come in handy,
        if logging files are still running.
        """
        p.join()

# %%
if __name__=="__main__":
    start_2_heads()
# %%
