#!/usr/bin/python
# -*- coding: utf-8 -*-

from aima.search import *
from nao_problem import NaoProblem
from utils import *
import time

class Move:
    def __init__(self, Moveduration=None):
        self.Moveduration = Moveduration
    
    def get(self):
        return self.Moveduration

def main(robot_ip, port):
    # Lista delle mosse utilizzate
    PossibleMoves = {
        'AirGuitar': Move(4.10),
        'DanceTwist': Move(6.49),
        'Handup': Move(10.73),
        'ArmDance': Move(10.42),
        'BlowKisses': Move(4.58),
        'Bow': Move(3.86),
        'DiagonalRight': Move(2.56),
        'DanceMove': Move(7.3),
        'SprinklerL': Move(4.6),
        'SprinklerR': Move(4.36),
        'RightArm': Move(9.19),
        'TheRobot': Move(7),
        'ComeOn': Move(3.62),
        'StayingAlive': Move(6.90),
        'Rhythm': Move(2.95),
        'Finger': Move(13),
        'PulpFiction': Move(5.80),
        'Wave': Move(3.72),
        'Clap': Move(4.73),
        'ArmsOpening': Move(8.15),
        'DiagonalLeft': Move(4.17),
        'DoubleMovement': Move(6.76),
        'Glory': Move(3.90),
        'Joy': Move(5.19),
        'MoveBackward': Move(4.79),
        'MoveForward': Move(3.75),
        'RotationFootLLeg': Move(7.50),
        'Union_arms': Move(10.31),
    }
    
    
    # Lista per tracciare le mosse già eseguite
    executed_moves = []

    # Posizioni iniziali, obbligatorie e finali
    starting_position = ('M_StandInit', Move(2.1))
    mandatory_position = [
        ('M_WipeForehead', Move(5.48)),
        ('M_Stand', Move(2.82)),
        ('M_Hello', Move(5.19)),
        ('M_Sit', Move(12.1)),
        ('M_SitRelax', Move(17.26)),
        ('M_StandZero', Move(1.4))
    ]
    final_position = ('M_Crouch', Move(1.32))

    pos_list = [starting_position, *mandatory_position, final_position]
    number_of_steps = len(pos_list) - 1


    # Calcolare il tempo totale per le mosse obbligatorie
    total_time = sum(pos[1].Moveduration for pos in pos_list)

    # Tempo totale per eseguire la mossa iniziale, le mosse mandatory e la mossa finale
    mandatory_time = total_time / number_of_steps

    # Fase di pianificazione
    print("PLANNED CHOREOGRAPHY:")
    solution = tuple()
    start_planning = time.time()
    last_move = None

    for index in range(1, len(pos_list)):
        # Pianificazione tra posizione di partenza e posizione finale
        starting_pos = pos_list[index - 1]
        ending_pos = pos_list[index]


        if ending_pos[0] in executed_moves:
            print(f"Skipping move {ending_pos[0]} as it was already executed.")
            print(f"Moves executed so far: {executed_moves}")
            continue  # Salta la mossa che è già stata eseguita

        choreography = (starting_pos[0],)  # Coreografia iniziale
        remaining_time = 110.0 / number_of_steps - mandatory_time

        cur_state = (
            ('choreography', choreography),
            ('remaining_time', remaining_time),
            ('moves_done', 0)
        )

        cur_goal_state = (
            ('remaining_time', 0),
            ('moves_done', 2)
        )

        keys = list(PossibleMoves.items())
        random.shuffle(keys)
        PossibleMoves = dict(keys)

        cur_problem = NaoProblem(cur_state, cur_goal_state, PossibleMoves, 1, solution)
        cur_solution = iterative_deepening_search(cur_problem)

        try:
            if cur_solution is None:
                raise RuntimeError(f'Step {index} - no solution was found!')
            cur_solution_dict = from_state_to_dict(cur_solution.state)
            cur_choreography = cur_solution_dict['choreography']
            print(f"Step {index}: \t" + ", ".join(cur_choreography))
            solution += cur_choreography
            # Aggiungi la mossa corrente alla lista delle mosse eseguite
            executed_moves.extend(cur_choreography)
            PossibleMoves = {move: details for move, details in PossibleMoves.items() if move not in executed_moves}
        except:
            print(f'Step {index}: solving just using the intermediate compulsory positions')
            for dance in pos_list[abs(index-2):-1]:
                solution+=(dance[0],)
            break
            

    # Fase di conclusione della pianificazione
    end_planning = time.time()
    solution += (final_position[0],)
    try:
        state_dict = from_state_to_dict(cur_solution.state)
        print("\nINFO:")
        print(f"Time required for the planning : %.2f seconds." % (end_planning - start_planning))
        print(f"Estimated choreography duration time: {110 - state_dict['remaining_time']}")
        print("-"*20)
    except AttributeError:
        times=sum(pos[1].Moveduration for pos in pos_list)
        i=0
        while i<len(solution):
            try:
                times+=PossibleMoves[dance].Moveduration
                i+=1
            except KeyError:
                i+=1

                

        print("\nINFO:")
        print(f"Time required for the planning : %.2f seconds." % (end_planning - start_planning))
        print(f"Estimated choreography duration time: {times}")
        print("-"*20)

    # Esecuzione della danza
    print("\nRunning...")
    play_song("Daft Punk - Something About Us.mp3")
    start_dance = time.time()
    do_moves(solution, robot_ip, port)
    end_dance = time.time()
    print(f"Real choreography duration time: %.2f seconds." % (end_dance - start_dance))

if __name__ == "__main__":
    robot_ip = "127.0.0.1"
    port = 9559  # Inserisci la porta NAO
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        robot_ip = sys.argv[1]
    elif len(sys.argv) == 2:
        robot_ip = sys.argv[1]
    
    main(robot_ip, port)