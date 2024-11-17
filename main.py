#!/usr/bin/python
# -*- coding: utf-8 -*-

from aima.search import *
from nao_problem import NaoProblem
from utils import *


def precondition_standing(position):
    if position == 'M_SitRelax':
        return False
    return True


def postcondition_standing(position):
    if position in ('M_Sit', 'M_SitRelax'):
        return False
    return True


class NaoMove:
    """
    This class defines the information related
    to a particular move.
    """
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = duration
        self.preconditions = preconditions if preconditions is not None else {}
        self.postconditions = postconditions if preconditions is not None else {}


def main(robot_ip, port):
    # TODO: win the challenge :-)
    # The following ones are the moves made available to the robot:
    moves = {
    'StandUp':       NaoMove(8.35,  {'standing': False}, {'standing': True}),
    'AirGuitar':     NaoMove(4.10,  {'standing': True},  {'standing': True}),
    'ArmDance':      NaoMove(10.42, {'standing': True},  {'standing': True}),
    'BlowKisses':    NaoMove(4.58,  {'standing': True},  {'standing': True}),
    'Bow':           NaoMove(3.86,  {'standing': True},  {'standing': True}),
    'DiagonalRight': NaoMove(2.56,  {'standing': True},  {'standing': True}),
    'DanceMove':     NaoMove(6.13,  {'standing': True},  {'standing': True}),
    'SprinklerL':    NaoMove(4.14,  {'standing': True},  {'standing': True}),
    'SprinklerR':    NaoMove(4.36,  {'standing': True},  {'standing': True}),
    'RightArm':      NaoMove(9.19,  None, None),
    'TheRobot':      NaoMove(6.10,  {'standing': True},  {'standing': True}),
    'ComeOn':        NaoMove(3.62,  {'standing': True},  {'standing': True}),
    'StayingAlive':  NaoMove(5.90,  {'standing': True},  {'standing': True}),
    'Rhythm':        NaoMove(2.95,  {'standing': True},  {'standing': True}),
    'PulpFiction':   NaoMove(5.80,  {'standing': True},  {'standing': True}),
    'Wave':          NaoMove(3.72,  None, None),
    'Glory':         NaoMove(3.28,  None, None),
    'Clap':          NaoMove(4.10,  None, None),
    'Joy':           NaoMove(4.50,  None, None),
    # Mosse aggiunte dalla lista moves non presenti in "moves" iniziale
    'ArmsOpening':   NaoMove(8.15,  {'standing': True},  {'standing': True}),
    'DiagonalLeft':  NaoMove(4.17,  {'standing': True},  {'standing': True}),
    'DoubleMovementGloryJoy': NaoMove(0.07, None, None),  # Mosse che hanno una durata estremamente breve
    'MoveBackward':  NaoMove(4.79,  {'standing': True},  {'standing': True}),
    'MoveForward':   NaoMove(3.75,  {'standing': True},  {'standing': True}),
    'RotationFootLLeg': NaoMove(7.50, {'standing': True},  {'standing': True}),
    'RotationFootRLeg': NaoMove(7.64, {'standing': True},  {'standing': True}),
    'Union_arms':    NaoMove(10.31, {'standing': True},  {'standing': True}),
    }

    # The following is the order we chose for the mandatory positions:
    initial_pos = ('M_StandInit',       NaoMove(1.60))
    mandatory_pos = [('M_WipeForehead', NaoMove(4.48)),
                     ('M_Stand',        NaoMove(2.32)),
                     ('M_Hello',        NaoMove(4.34)),
                     ('M_Sit',          NaoMove(9.84)),
                     ('M_SitRelax',     NaoMove(3.92)),
                     ('M_StandZero',    NaoMove(1.4))]
    final_goal_pos = ('M_Crouch',       NaoMove(1.32))
    pos_list = [initial_pos, *mandatory_pos, final_goal_pos]
    number_of_steps = len(pos_list) - 1
    # Lista per tracciare le mosse già eseguite
    executed_moves = []
    # Here we compute the total time lost during the
    # entire choreography for the execution of mandatory moves
    total_time = 0.0
    for pos in pos_list:
        total_time += pos[1].duration
    # We consider 'total_time' as being
    # evenly spread over each planning step:
    mean_time_lost_because_of_mandatory_positions = total_time / number_of_steps

    # Planning phase of the algorithm
    solution = tuple()
    print("PLANNED CHOREOGRAPHY:")
    start_planning = time.time()
    last_move = None
    for index in range(1, len(pos_list)):
        # The planning is done in several distinct steps: each
        # one of them consists in solving a tree search in the space
        # of possible choreographies between a mandatory position
        # and the next one.
        starting_pos = pos_list[index - 1]
        ending_pos = pos_list[index]
        if ending_pos[0] in executed_moves:
            print(f"Skipping move {ending_pos[0]} as it was already executed.")
            print(f"Moves executed so far: {executed_moves}")
            continue  # Salta la mossa che è già stata eseguita

        choreography = (starting_pos[0],)  # Initial choreography
        initial_standing = postcondition_standing(starting_pos[0])
        goal_standing = precondition_standing(ending_pos[0])
        remaining_time = 180.0/number_of_steps - mean_time_lost_because_of_mandatory_positions
        cur_state = (('choreography', choreography),
                     ('standing', initial_standing),
                     ('remaining_time', remaining_time),
                     ('moves_done', 0))
        cur_goal_state = (('standing', goal_standing),
                          ('remaining_time', 0),  # About this amount of time left
                          ('moves_done', 3))  

        cur_problem = NaoProblem(cur_state, cur_goal_state, moves, 1, solution)
        cur_solution = iterative_deepening_search(cur_problem)
        if cur_solution is None:
            raise RuntimeError(f'Step {index} - no solution was found!')

        cur_solution_dict = from_state_to_dict(cur_solution.state)
        cur_choreography = cur_solution_dict['choreography']
        print(f"Step {index}: \t" + ", ".join(cur_choreography))
        solution += cur_choreography
        # Aggiungi la mossa corrente alla lista delle mosse eseguite
        executed_moves.append(ending_pos[0]) 

    end_planning = time.time()
    solution += (final_goal_pos[0],)
    state_dict = from_state_to_dict(cur_solution.state)
    print("\nSTATISTICS:")
    print(f"Time required by the planning phase: %.2f seconds." % (end_planning-start_planning))
    print(f"Estimated choreography duration: {180.0 - state_dict['remaining_time']}")
    print("-------------------------------------------------------")
    
    # Dance execution
    print("\nDANCE EXECUTION:")
    play_song("Don't stop me now - Queen.mp3")
    start_dance = time.time()
    do_moves(solution, robot_ip, port)
    end_dance = time.time()
    print("Length of the entire choreography: %.2f seconds." % (end_dance-start_dance))


if __name__ == "__main__":

    robot_ip = "127.0.0.1"
    port = 9559  # Insert NAO port
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        robot_ip = sys.argv[1]
    elif len(sys.argv) == 2:
        robot_ip = sys.argv[1]
    
    main(robot_ip, port)