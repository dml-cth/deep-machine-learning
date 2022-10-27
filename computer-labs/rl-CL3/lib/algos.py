import numpy as np


def policy_evaluation_one_step(env, policy, value_table, gamma=0.9):
    # For each state
    for s_idx, s in enumerate(env.states):
        if env.terminal_table[s_idx] == 1:
            value_table[s_idx] = 0
            continue

        new_v = 0
        # For each action
        for a in range(4):
            pi_prob = policy[s_idx, a]
            s_prime_pmf = env.transition_table[s_idx, a]
            # For each possible next state
            for s_prime_idx, trans_prob in enumerate(s_prime_pmf):
                r = env.reward_table[s_idx, a]
                if env.terminal_table[s_prime_idx] == 0:
                    new_v += pi_prob * trans_prob * (r + gamma * value_table[s_prime_idx])
                else:
                    new_v += pi_prob * trans_prob * r
        value_table[s_idx] = new_v


def policy_improvement(env, policy, value_table, gamma=0.9):

    for i_s, s in enumerate(env.states):
        # Initialize q-values for current state and new policy
        q = np.zeros(4)
        new_policy = np.zeros(4)

        # Compute q-value for each action in current state
        for a in range(4):
            r = env.reward_table[i_s, a]
            next_s_pmf = env.transition_table[i_s, a]
            for i_next_s, prob in enumerate(next_s_pmf):
                q[a] += prob * (r + gamma * value_table[i_next_s])

        # Set policy to greedy w.r.t. Q-values computed above
        new_policy[np.argmax(q)] = 1
        policy[i_s] = new_policy


def epsilon_greedy_pi_from_q_table(env, q_table, epsilon):
    policy = np.zeros((len(env.states), 4))
    for i_s, s in enumerate(env.states):
        q_values = q_table[i_s]
        a_star = np.argmax(q_values)
        policy[i_s, :] = [epsilon/4]*4
        policy[i_s, a_star] += 1-epsilon
    return policy


if __name__ == '__main__':
    from lib.grid_world import grid_world_3x3 as env
    from lib.plot_utils import plot_policy, plot_value_table
    import matplotlib.pyplot as plt

    np.random.seed(2)
    env.reset()
    value_table = np.random.rand(130)
    policy = np.ones((len(env.states), 4)) * 0.25
    for i, s in enumerate(env.states):
        policy[i, :] = np.random.dirichlet([0.1, 0.1, 0.1, 0.1])

    plot_value_table(env, value_table)
    plot_policy(env, policy)
    plt.show()