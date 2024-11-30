
import time 
import subprocess
import vlc
import sys
import random
def play_song(song_name):
    p = vlc.MediaPlayer(song_name)
    p.play()


class Moves:
    def __init__(self, name):

        self.name=name
   
    def execute(self, robot_port=9559, robot_ip="127.0.0.1"):
        python2_command = f"python2 ./NaoMoves/{self.name}.py  {robot_ip} {robot_port}"
        subprocess.run(python2_command.split(), stdout=subprocess.PIPE)
        # print(process.stdout) # receive output from the python2 script

def exec_dur(move):
    start=time.time()
    move.execute()
    end=time.time()
    print(round(end-start,2))
    return round(end-start,2)