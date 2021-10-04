from collections import namedtuple
import numpy as np

def test_policy(pi):
    
    pi[4] = 0 # green state
    pi[9] = 0 # red state
    pi[6] = 0 # unreachable state 
    pi[7] = 0 # unreachable state
    pi_star = np.array([ 3.,  3.,  3.,  3.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.,  1.,  1.,  2.,  0.])
    assert np.array_equal(pi, pi_star), "Failed, policy is not optimal"
    print('Passed: policy test, for gamma=.99')

def test_state_values(V):

    v_star = np.array([ 0.93861973,  0.95193393,  0.9639533,   0.97612443,  1.,
                        0.92691625,  0.,          0.,          0.88371826, -1.,
                        0.91395196,  0.90255605,  0.89130223,  0.88057656,  0.79978972,
                        0])

    assert (sum(abs(V - v_star)) < 1e-4), "Failed, not correct state-values"
    print('Passed: state-value test, for gamma=.99')
    
def test_value_iteration(V, pi):
    test_state_values(V)
    test_policy(pi)
    
def test_q_learning(Q):
    pi = [np.argmax(Q[i]) for i in range(len(Q[:]))]
    test_policy(pi)


class GridWorldMDP(object):
    def __init__(self, trans_prob=.8):
        '''
        Initializes an instance of the GridWorldMDP class
        :param trans_prob: transition probabilities (e.g. =1 for deterministic MDP)
        '''
        assert 0 <= trans_prob and trans_prob <= 1., "Not a valid transition probability"
        # actions {0=N, 1=W, 2=S, 3}
        # available actions: North, West, South, East
        self.__actions_to_char = {i: char for i, char in enumerate(['↑', '←', '↓', '→'])}
        self.__num_actions = 4
        self.__actions = np.arange(self.__num_actions)
        self._transition_model = self.__transition_model(trans_prob)
        self._num_states = np.shape(self._transition_model)[1]        
        self._init_state = 10 # init state in lower left corner
        self._state = self._init_state
        self._states = np.arange(self._num_states)

    def get_states(self):
        '''
        Returns complete set of states for the MDP
        :return: numpy array of shape [num states,]
        '''
        return self._states

    def get_actions(self):
        '''
        Returns complete set of actions for the MDP
        :return: numpy array of shape [num actions,]
        '''
        return self.__actions

    @property
    def act_to_char_dict(self):
        '''
        Returns dictionary that points action to char, i,e. N, W, S, E
        '''
        return self.__actions_to_char

    def reset(self):
        '''
        Resets the environment and the agent is positioned in the initial state in the bottom left corner.
        :return: state, reward, terminal
        '''
        self._state = self._init_state
        return self._state, 0, False

    def step(self, action):
        '''
        Takes one step in the environment using the selected action
        :param action: action to execute, integer
        :return: state, reward, terminal
        '''
        trans_prob = self.state_transition_func(self._state, action)
        new_state = np.random.choice(self._num_states, p=trans_prob)
        reward = 0
        terminal = self._state == 15
        reward = self.reward_function(self._state, action)
        self._state = new_state
        return new_state, reward, terminal

    def __transition_model(self, p=.8):

        p_ = (1-p) / 2
        return np.array([ #NORTH
                          [[p + p_, p_, 0, 0, 0,  0, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0],
                          [p_, p, p_, 0, 0,    0, 0, 0, 0, 0,      0, 0, 0, 0, 0,   0],
                          [0, p_, p, p_, 0,    0, 0, 0, 0, 0,      0, 0, 0, 0, 0,   0],
                          [0, 0, p_, p, p_,    0, 0, 0, 0, 0,      0, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,      0, 0, 0, 0, 0,   1], # green state

                          [p, 0, 0, 0, 0,    2 * p_, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,        0, 1, 0, 0, 0,    0, 0, 0, 0, 0,   0], # ureachable
                          [0, 0, 0, 0, 0,        0, 0, 1, 0, 0,    0, 0, 0, 0, 0,   0], # ureachable
                          [0, 0, 0, p, 0,        0, 0,0 , p_, p_,  0, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,        0, 0, 0, 0, 0,    0, 0, 0, 0, 0,   1], # red state

                          [0, 0, 0, 0, 0,       p, 0, 0, 0, 0,   p_, p_, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,   p_, p, p_, 0, 0,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,   0, p_, p, p_, 0,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, p, 0,   0, 0, p_, 0, p_,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, p,   0, 0, 0, p_, p_,   0],

                          [0, 0, 0, 0, 0,        0, 0, 0, 0, 0,    0, 0, 0, 0, 0,   1] # terminal state loop

                          ], # WEST
                         [[p + p_, 0, 0, 0, 0,   p_, 0, 0, 0, 0,  0, 0, 0, 0, 0,   0],
                          [p, 2 * p_, 0, 0, 0,   0, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0],
                          [0, p, 2 * p_, 0, 0,   0, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0],
                          [0, 0, p, 2* p_, 0,    0, 0, 0, 0, 0,   0, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     0, 0, 0, 0, 0,   1], # green state

                          [p_, 0, 0, 0, 0,      p, 0, 0, 0, 0,   p_, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,       0, 1, 0, 0, 0,   0, 0, 0, 0, 0,    0], # unreachable
                          [0, 0, 0, 0, 0,       0, 0, 1, 0, 0,   0, 0, 0, 0, 0,    0], # unreachable
                          [0, 0, 0, p_, 0,      0, 0, 0, p, 0,   0, 0, 0, p_, 0,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,   0, 0, 0, 0, 0,    1], # red state

                          [0, 0, 0, 0, 0,      p_, 0, 0, 0, 0,    p + p_, 0, 0, 0, 0,  0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,    p, 2 * p_, 0, 0, 0,  0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,    0, p, 2 * p_, 0, 0,  0],
                          [0, 0, 0, 0, 0,       0, 0, 0, p_, 0,    0, 0, p, p_, 0,     0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, p_,    0, 0, 0,  p, p_,    0],

                          [0, 0, 0, 0, 0,        0, 0, 0, 0, 0,    0, 0, 0, 0, 0,   1] # terminal state loop
                          ], # SOUTH
                         [[p_, p_, 0, 0, 0,     p, 0, 0, 0, 0,     0, 0, 0, 0, 0,   0],
                          [p_, p, p_, 0, 0,     0, 0, 0, 0, 0,     0, 0, 0, 0, 0,   0],
                          [0, p_, p, p_, 0,     0, 0, 0, 0, 0,     0, 0, 0, 0, 0,   0],
                          [0, 0, p_, 0, p_,     0, 0, 0, p, 0,     0, 0, 0, 0, 0,   0],
                          [0, 0, 0, 0, 0,       0, 0, 0, 0, 0,     0, 0, 0, 0, 0,   1], # green state

                          [0, 0, 0, 0, 0,    2 * p_, 0, 0, 0, 0,  p, 0, 0, 0, 0,    0],
                          [0, 0, 0, 0, 0,      0, 1, 0, 0, 0,     0, 0, 0, 0, 0,    0], # unreachable state
                          [0, 0, 0, 0, 0,      0, 0, 1, 0, 0,     0, 0, 0, 0, 0,    0], # unreachable state
                          [0, 0, 0, 0, 0,      0, 0, 0, p_, p_,   0, 0, 0, p, 0,    0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     0, 0, 0, 0, 0,    1], # red state

                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     p + p_, p_, 0, 0, 0,  0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     p_, p, p_, 0, 0,  0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     0, p_, p, p_, 0,  0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     0, 0, p_, p, p_,  0],
                          [0, 0, 0, 0, 0,      0, 0, 0, 0, 0,     0, 0, 0, p_, p + p_,  0],

                          [0, 0, 0, 0, 0,        0, 0, 0, 0, 0,    0, 0, 0, 0, 0,   1] # terminal state loop
                          ], 
                          # EAST
                          [[p_, p, 0, 0, 0,    p_, 0, 0, 0, 0,   0, 0, 0, 0, 0,     0],
                           [0, 2*p_, p, 0, 0,  0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     0],
                           [0, 0, 2*p_, p, 0,  0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     0],
                           [0, 0, 0, p_, p,    0, 0, 0, p_, 0,   0, 0, 0, 0, 0,     0],
                           [0, 0, 0, 0, 0,     0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     1], # green state

                           [p_, 0, 0, 0, 0,    p, 0, 0, 0, 0,    p_, 0, 0, 0, 0,    0],
                           [0, 0, 0, 0, 0,     0, 1, 0, 0, 0,    0, 0, 0, 0, 0,     0], # unreachable state
                           [0, 0, 0, 0, 0,     0, 0, 1, 0, 0,    0, 0, 0, 0, 0,     0], # unreachable state
                           [0, 0, 0, p_, 0,    0, 0, 0, 0, p,    0, 0, 0, p_, 0,    0],
                           [0, 0, 0, 0, 0,     0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     1], # red state

                           [0, 0, 0, 0, 0,    p_, 0, 0, 0, 0,    p_, p, 0, 0, 0,        0],
                           [0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     0, 2 * p_, p, 0, 0,    0],
                           [0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     0, 0, 2 * p_, p, 0,    0],
                           [0, 0, 0, 0, 0,    0, 0, 0, p_, 0,    0, 0, 0, p_, p,        0],
                           [0, 0, 0, 0, 0,    0, 0, 0, 0, p_,    0, 0, 0, 0, p + p_,    0],
                           
                           [0, 0, 0, 0, 0,    0, 0, 0, 0, 0,     0, 0, 0, 0, 0,   1] # terminal state loop
                           ]])

    
    
    def state_transition_func(self, s, a):
        '''
        Returns the transition probabilities to all states given current state and action
        :param state: current state as integer
        :param action: selected action as integer
        :return: state-transition probabilities, i.e.
         [P[S_0| S=s, A_t=a], P[S_1| S=s, A=a], ..., P[S_14| S=s, A=a]]
        '''
        return np.array(self._transition_model[a, s])

    def reward_function(self, s, a):
        '''
        Returns the reward r(s,a)
        :param state: current state as integer
        :param action: selected action as integer
        :return: r(s,a)
        '''
        if s ==4: 
            return 1 # green state
        elif s==9:
            return -1 # red state
        else: 
            return 0
