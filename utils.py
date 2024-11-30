#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import subprocess
import time
from classes import Moves
import vlc


def play_song(song_name):
    p = vlc.MediaPlayer(song_name)
    p.play()


def do_moves(moves, robot_ip, robot_port):
    # Here we execute all the given moves
    # in a Python2 environment.
    for i in range(len(moves)):
        print(f"Executing: {moves[i]}... ", end="", flush=True)
        if moves[i-1]=='M_Sit' or moves[i-1]=='M_SitRelax':
            Moves('stands').execute()
        python2_command = f"python2 ./NaoMoves/{moves[i]}.py  {robot_ip} {robot_port}"
        start_move = time.time()
        subprocess.run(python2_command.split(), stdout=subprocess.PIPE)
        end_move = time.time()
        # print(process.stdout) # receive output from the python2 script
        print("done in %.2f seconds." % (end_move-start_move), flush=True)


def from_state_to_dict(state):
    """
    Converts a state into a dictionary for easier access to the key-value pairs.

    """
    params_dict = dict()
    for t in state:
        len_t = len(t)
        if len_t < 2:
            continue
        key = t[0]
        if len_t > 2:
            value = t[1:]
        else:
            value = t[1]
        if key not in params_dict:
            params_dict[key] = value
    return params_dict
