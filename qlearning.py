'''
Just a simple example from http://mnemstudio.org/path-finding-q-learning-tutorial.htm
'''

import numpy as np
from random import randint

def compute_q(current_state, next_state, possible_states_from_next_state):
    q_values_from_possible_state_from_next_state = [ q_values[next_state][possible_state] for possible_state in possible_states_from_next_state]
    return r_values[current_state][next_state] + gamma * max( q_values_from_possible_state_from_next_state )

def find_path(initial_state, q_values):
    current_state = initial_state

    steps = [current_state]

    while current_state != final_state:
        current_state = np.where(q_values[current_state] == q_values[current_state].max())[0][0]
        steps.append(current_state)

    return steps

if __name__ == '__main__':

    q_values = np.zeros((6,6))
    r_values = np.array([[-1, -1, -1, -1, 0, -1],
                        [-1, -1, -1, 0, -1, 100],
                        [-1, -1, -1, 0, -1, -1],
                        [-1, 0, 0, -1, 0, -1],
                        [0, -1, -1, 0, -1, 100],
                        [-1, 0, -1, -1, 0, 100]])

    gamma = 0.8 #learning rate

    final_state = 5
    
    for i in range(100):
        current_state = randint(0,5)
    
        print('initial state {}'.format(current_state))

        goal_reached = False

        while not goal_reached:
    
            possible_states = np.where(r_values[current_state] != -1)[0]
        
            print('possible next {}'.format(possible_states))

            next_state = possible_states[randint(0, len(possible_states)-1)]

            print('selected next state {}'.format(next_state))

            possible_states_from_next_state = np.where(r_values[next_state] != -1)[0]

            print('next of next {}'.format(possible_states_from_next_state))

            q_values[current_state][next_state] = compute_q(current_state, next_state, possible_states_from_next_state)        

            current_state = next_state
            goal_reached = next_state == final_state
        
    print(q_values)

    print('normalizing matrix')

    max_q = q_values.max()
    factor = 100.0 / max_q

    q_values = q_values * factor

    print(q_values)

    print('example using q matrix')

    initial_state = 2
    print('steps from {} to 5:  {}'.format(initial_state, find_path(initial_state, q_values)))

    initial_state = 0
    print('steps from {} to 5:  {}'.format(initial_state, find_path(initial_state, q_values)))
