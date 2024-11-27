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
    # Dizionario delle mosse disponibili con la relativa durata
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
    
    # Lista per tracciare le mosse già eseguite durante la coreografia
    executed_moves = []

    # Posizioni iniziali, obbligatorie e finali
    initial_position = ('M_StandInit', Move(2.1))
    mandatory_positions = [
        ('M_WipeForehead', Move(5.48)),
        ('M_Stand', Move(2.82)),
        ('M_Hello', Move(5.19)),
        ('M_Sit', Move(12.1)),
        ('M_SitRelax', Move(17.26)),
        ('M_StandZero', Move(1.4))
    ]
    final_position = ('M_Crouch', Move(1.32))

    # Lista di tutte le posizioni della coreografia
    choreography_positions = [initial_position, *mandatory_positions, final_position]
    number_of_steps = len(choreography_positions) - 1

    # Calcolo del tempo totale delle mosse obbligatorie
    total_time = sum(pos[1].Moveduration for pos in choreography_positions)

    # Tempo medio per ogni fase della coreografia
    average_mandatory_time = total_time / number_of_steps

    # Fase di pianificazione della coreografia
    print("PLANNED CHOREOGRAPHY:")
    choreography_solution = tuple()  # Soluzione finale della coreografia
    planning_start_time = time.time()  # Tempo di inizio pianificazione
    last_move = None

    for index in range(1, len(choreography_positions)):
        # Pianificazione tra posizione iniziale e posizione successiva
        starting_position = choreography_positions[index - 1]
        ending_position = choreography_positions[index]

        if ending_position[0] in executed_moves:
            print(f"Skipping move {ending_position[0]} as it was already executed.")
            print(f"Moves executed so far: {executed_moves}")
            continue  # Salta la mossa già eseguita

        # Creazione stato iniziale e obiettivo per la pianificazione
        initial_state = (
            ('choreography', (starting_position[0],)),
            ('remaining_time', 110.0 / number_of_steps - average_mandatory_time),
            ('moves_done', 0)
        )
        goal_state = (
            ('remaining_time', 0),
            ('moves_done', 2)
        )

        # Mescolare le mosse disponibili per aumentare la varietà
        keys = list(PossibleMoves.items())
        random.shuffle(keys)
        PossibleMoves = dict(keys)

        # Creazione del problema e ricerca della soluzione
        nao_problem = NaoProblem(initial_state, goal_state, PossibleMoves, 1, choreography_solution)
        nao_solution = iterative_deepening_search(nao_problem)

        try:
            if nao_solution is None:
                raise RuntimeError(f'Step {index} - no solution was found!')
            solution_state_dict = from_state_to_dict(nao_solution.state)
            current_choreography = solution_state_dict['choreography']
            print(f"Step {index}: \t" + ", ".join(current_choreography))
            choreography_solution += current_choreography
            executed_moves.extend(current_choreography)
            PossibleMoves = {move: details for move, details in PossibleMoves.items() if move not in executed_moves}
        except:
            print(f'Step {index}: solving using intermediate compulsory positions')
            for dance in choreography_positions[abs(index - 2):-1]:
                choreography_solution += (dance[0],)
            break
            
    # Fase di conclusione della pianificazione
    planning_end_time = time.time()
    choreography_solution += (final_position[0],)
    try:
        state_dict = from_state_to_dict(nao_solution.state)
        print("\nINFO:")
        print(f"Time required for the planning : %.2f seconds." % (planning_end_time - planning_start_time))
        print(f"Estimated choreography duration time: {110 - state_dict['remaining_time']}")
        print("-" * 20)
    except AttributeError:
        total_duration = sum(pos[1].Moveduration for pos in choreography_positions)
        print("\nINFO:")
        print(f"Time required for the planning : %.2f seconds." % (planning_end_time - planning_start_time))
        print(f"Estimated choreography duration time: {total_duration}")
        print("-" * 20)

    # Esecuzione della coreografia
    print("\nRunning...")
    play_song("Daft Punk - Something About Us.mp3")
    dance_start_time = time.time()
    do_moves(choreography_solution, robot_ip, port)
    dance_end_time = time.time()
    print(f"Real choreography duration time: %.2f seconds." % (dance_end_time - dance_start_time))

if __name__ == "__main__":
    robot_ip = "127.0.0.1"
    port = 9559  # Inserisci la porta NAO
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        robot_ip = sys.argv[1]
    elif len(sys.argv) == 2:
        robot_ip = sys.argv[1]
    
    main(robot_ip, port)
