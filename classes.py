
import time 
import subprocess
import vlc
import sys

def play_song(song_name):
    p = vlc.MediaPlayer(song_name)
    p.play()

class Move:
    def __init__(self, name, duration):
        '''
        Create a class to define the moves using the name and its duration 
        '''

        self.name=name
        self.duration=duration

    def __len__(self):
        '''
        function to return duration of the move just using len
        '''
        return self.duration
    
    def execute(self, robot_port=9559, robot_ip="127.0.0.1"):
        '''
        Function to execute the move on the robot
        '''
        python2_command = f"python2 ./NaoMoves/{self.name}.py  {robot_ip} {robot_port}"
        start_move = time.time()
        subprocess.run(python2_command.split(), stdout=subprocess.PIPE)
        end_move = time.time()
        # print(process.stdout) # receive output from the python2 script
        print("done in %.2f seconds." % (end_move-start_move), flush=True)



g=Move('AirGuitar', 4.1)
g.execute()
