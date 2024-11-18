

import time 
import subprocess
import vlc
import sys
import random
def play_song(song_name):
    p = vlc.MediaPlayer(song_name)
    p.play()

class NaoMove:
    """
    This class defines the information related
    to a particular move.
    """
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = duration
        self.preconditions = preconditions if preconditions is not None else {}
        self.postconditions = postconditions if preconditions is not None else {}

    def __str__(self):
        return 'NaoMove('+str(self.duration)+','+str(self.preconditions)+','+str(self.postconditions)+')'
    
    def get(self):
        return 'NaoMove('+str(self.duration)+','+str(self.preconditions)+','+str(self.postconditions)+')'

class Move:
    def __init__(self, name):
        '''
        Create a class to define the moves using the name and its duration 
        '''

        self.name=name
   
    def execute(self, robot_port=9559, robot_ip="127.0.0.1"):
        python2_command = f"python2 ./NaoMoves/{self.name}.py  {robot_ip} {robot_port}"
        start_move = time.time()
        subprocess.run(python2_command.split(), stdout=subprocess.PIPE)
        end_move = time.time()
        # print(process.stdout) # receive output from the python2 script
        print("done in %.2f seconds." % (end_move-start_move), flush=True)
    end=time.time()

def exec_dur(move):
    start=time.time()
    move.execute()
    end=time.time()
    return round(end-start,2)
    
moves=['AirGuitar', 'ArmDance', 'ArmsOpening', 'M_Sit','BlowKisses', 'Bow', 'Clap', 'ComeOn', 'DanceMove', 
       'DiagonalLeft','DiagonalRight','DoubleMovement','Glory',
        'Joy', 'M_Crouch', 'M_Hello',  'M_SitRelax', 'M_StandZero',
        'M_Stand',  'M_WipeForehead', 
        'MoveBackward', 'MoveForward', 'PulpFiction', 'Rhythm', 'RightArm', 
        'RotationFootLLeg',  'M_StandInit', 'RotationFootRLeg', 'SprinklerL', 'SprinklerR',
          'StandUp', 'StayingAlive', 'TheRobot', 'Union_arms', 'Wave']

Move('Joy').execute()
