import numpy as np


class GridWorld:
    def __init__(
        self, states, initial_state, transition_table, reward_table, terminal_table
    ):
        self.states = states
        self.initial_state = initial_state
        self.transition_table = transition_table
        self.reward_table = reward_table
        self.terminal_table = terminal_table
        self.state = None

    def step(self, a):
        s = self.state
        assert (
            self.terminal_table[self.states.index(s)] != 1
        ), "Trying to step from a terminal state."
        possible_s_primes_idxs = self.transition_table[self.states.index(s), a]
        s_prime_idx = np.random.choice(len(self.states), p=possible_s_primes_idxs)
        s_prime = self.states[s_prime_idx]
        r = self.reward_table[self.states.index(s), a]
        t = self.terminal_table[self.states.index(s_prime)]

        self.state = s_prime
        return s_prime, r, t

    def reset(self):
        self.state = self.initial_state
        return self.state[:]


a_index_to_symbol = {0: "\u2191", 1: "\u2192", 2: "\u2193", 3: "\u2190"}


def get_next_s(s, a, states):
    # Up
    if a == 0:
        next_s = [s[0], s[1] + 1]
    # Right
    elif a == 1:
        next_s = [s[0] + 1, s[1]]
    # Down
    elif a == 2:
        next_s = [s[0], s[1] - 1]
    # Left
    elif a == 3:
        next_s = [s[0] - 1, s[1]]
    else:
        raise ValueError(f"Action {a} not supported. Allowed values are [0, 1, 2, 3].")

    return next_s if next_s in states else s


def get_next_s_idx(s, a, states):
    return states.index(get_next_s(s, a, states))


def get_pmf_possible_s_primes(env, s, a):
    """
    Returns a pmf over the states which it's possible to transition to from state s when performing action a.

    Returns:
        possible_s_prime_idxs: List of indexes of the possible next states (to be used to index env.states).
        s_pmf: List of numbers ]0, 1] corresponding to the probability of transitioning to the states in
            possible_s_prime_idxs.
    """
    s_pmf = env.transition_table[env.states.index(s), a]
    possible_s_prime_idxs = np.argwhere(s_pmf > 0.001).flatten()
    return possible_s_prime_idxs, s_pmf[possible_s_prime_idxs]


def create_default_transition_table(states):
    transition_table = np.zeros((len(states), 4, len(states)))
    for i_s, s in enumerate(states):
        for a in range(4):
            s_prime = get_next_s(s, a, states)
            transition_table[i_s, a, states.index(s_prime)] = 1
    return transition_table


def create_stochastic_transition_table(states):
    transition_table = np.zeros((len(states), 4, len(states)))
    for i_s, s in enumerate(states):
        for a in range(4):
            for outcome_a in range(4):
                if a == outcome_a:
                    transition_table[i_s, a, get_next_s_idx(s, outcome_a, states)] += (
                        0.7
                    )
                else:
                    transition_table[i_s, a, get_next_s_idx(s, outcome_a, states)] += (
                        0.1
                    )
    return transition_table


# Deterministic 3x3 gridworld
states = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
transition_table = create_default_transition_table(states)
reward_table = -np.ones((len(states), 4))
terminal_table = np.zeros(len(states))
terminal_table[-1] = 1
grid_world_3x3 = GridWorld(
    states=states,
    initial_state=[0, 0],
    transition_table=transition_table,
    reward_table=reward_table,
    terminal_table=terminal_table,
)

# Deterministic 2x2 gridworld
states = [[0, 0], [0, 1], [1, 0], [1, 1]]
transition_table = create_default_transition_table(states)
reward_table = -np.ones((len(states), 4))
terminal_table = np.zeros(len(states))
terminal_table[-1] = 1
grid_world_2x2 = GridWorld(
    states=states,
    initial_state=[0, 0],
    transition_table=transition_table,
    reward_table=reward_table,
    terminal_table=terminal_table,
)

# Random 3x3 gridworld
states = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
transition_table = create_stochastic_transition_table(states)
reward_table = -np.ones((len(states), 4))
terminal_table = np.zeros(len(states))
terminal_table[-1] = 1
grid_world_3x3_stoch = GridWorld(
    states=states,
    initial_state=[0, 0],
    transition_table=transition_table,
    reward_table=reward_table,
    terminal_table=terminal_table,
)

# Random line-gridworld
states = [[0, 0], [1, 0], [2, 0]]
transition_table = create_stochastic_transition_table(states)
reward_table = -np.ones((len(states), 4))
terminal_table = np.zeros(len(states))
terminal_table[-1] = 1
grid_world_line_stoch = GridWorld(
    states=states,
    initial_state=[0, 0],
    transition_table=transition_table,
    reward_table=reward_table,
    terminal_table=terminal_table,
)


def create_3x3_env_randomly_permuted_actions(stochastic=False):
    """
    Creates a 3x3 grid-world where actions work differently for each state.
    """

    states = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    if stochastic:
        transition_table = create_stochastic_transition_table(states)
    else:
        transition_table = create_default_transition_table(states)

    # Randomly permute what actions do in each state
    for s_i in range(len(states)):
        transition_table[s_i] = np.random.permutation(transition_table[s_i])

    reward_table = -np.ones((len(states), 4))
    terminal_table = np.zeros(len(states))
    terminal_table[-1] = 1
    grid_world = GridWorld(
        states=states,
        initial_state=[0, 0],
        transition_table=transition_table,
        reward_table=reward_table,
        terminal_table=terminal_table,
    )
    return grid_world
