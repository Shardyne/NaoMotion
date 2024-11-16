

import time 
import subprocess
import vlc
import sys
import random
def play_song(song_name):
    p = vlc.MediaPlayer(song_name)
    p.play()

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
       'DiagonalLeft','DiagonalRight','DoubleMovement' 'Glory'
        'Joy', 'M_Crouch', 'M_Hello',  'M_SitRelax', 'M_StandZero',
        'M_Stand',  'M_WipeForehead', 
        'MoveBackward', 'MoveForward', 'PulpFiction', 'Rhythm', 'RightArm', 
        'RotationFootLLeg',  'M_StandInit', 'RotationFootRLeg', 'SprinklerL', 'SprinklerR',
          'StandUp', 'StayingAlive', 'TheRobot', 'Union_arms', 'Wave']

moves_dur={'AirGuitar': 5.4, 'SprinklerL': 5.08, 'M_Stand': 3.45, 'Rhythm': 4.97, 
 'M_StandZero': 2.77, 'SprinklerR': 5.19, 'BlowKisses': 5.27, 'M_Crouch': 1.65, 
 'Union_arms': 10.31, 'M_Sit': 11.37, 'StayingAlive': 11.93, 'Wave': 5.99,
   'DiagonalLeft': 4.17, 'M_SitRelax': 15.46, 'RightArm': 14.26, 'DiagonalRight': 6.46, 
   'ComeOn': 5.35, 'MoveBackward': 4.79, 'MoveForward': 3.75, 'M_WipeForehead': 5.44, 
   'RotationFootLLeg': 7.5, 'PulpFiction': 6.83, 'TheRobot': 7.56, 'M_StandInit': 1.96, 
   'Clap': 4.99, 'Bow': 4.81, 'ArmDance': 13.03, 'ArmsOpening': 8.15, 'RotationFootRLeg': 7.64,
     'StandUp': 1.21, 'DanceMove': 7.49, 'DoubleMovementGloryJoy': 0.07, 'M_Hello': 5.47}


random.shuffle(moves)

for dance in moves:
    moves_dur[dance]=exec_dur(Move(dance))
print(moves_dur)
