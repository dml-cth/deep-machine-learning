import matplotlib.pyplot as plt
import numpy as np

from lib.algos import epsilon_greedy_pi_from_q_table
from lib.plot_utils import plot_all_states, plot_agent, plot_q_table, plot_env_agent_and_policy_at_state, \
    plot_env_agent_and_chosen_action, plot_policy
from lib.grid_world import a_index_to_symbol


class QLearning:
    def __init__(self, env, initial_q_table, alpha=0.2, initial_epsilon=1.00, vmin=-8, vmax=0.5):
        self.env = env
        self.q_table = initial_q_table
        self.alpha = alpha
        self.epsilon = initial_epsilon
        self.vmin = vmin
        self.vmax = vmax

        self.exploratory_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, self.epsilon)
        self.greedy_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, 0.0)

        self.fig, self.ax = None, None
        self.phase = 'choosing_actions'
        self.sampled_a = None
        self.current_transition = []

        self.env.reset()

    @property
    def s(self):
        return self.env.state

    @property
    def s_idx(self):
        return self.env.states.index(self.s)

    @property
    def s_centered(self):
        return [self.s[0] + 0.5, self.s[1] + 0.5]

    def next_step(self, fast_execution=False):
        print_string = ''
        if self.phase == 'choosing_actions':
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_policy_at_state(self.env, self.s, self.exploratory_policy, self.ax[0])
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()
                print('Sampling action...\n')

            self.phase = 'showing_sampled_action'

        elif self.phase == 'showing_sampled_action':
            self.sampled_a = np.random.choice(4, p=self.exploratory_policy[self.s_idx])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(self.env, self.s, self.sampled_a, self.ax[0])
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()
                print(f'Action sampled: {a_index_to_symbol[self.sampled_a]}\n')

            self.phase = 'carrying_out_action'

        elif self.phase == 'carrying_out_action':
            old_s = self.s
            s_prime, r, t = self.env.step(self.sampled_a)
            self.current_transition = [old_s, self.sampled_a, r, s_prime, t]

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_agent(self.s, self.ax[0])
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()
                print(f'Action sampled: {a_index_to_symbol[self.sampled_a]}\n')

            if t:
                if not fast_execution:
                    print('A terminal state has been reached: end of episode.')
                self.phase = 'update_q_value_terminal'
            else:
                self.phase = 'computing_td_target'

        elif self.phase == 'computing_td_target':
            # Compute TD target
            s, a, r, s_prime, _ = self.current_transition
            s_prime_idx = self.env.states.index(s_prime)
            greedy_a = np.random.choice(4, p=self.greedy_policy[self.s_idx])
            td_target = r + 0.9 * self.q_table[s_prime_idx, greedy_a]

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()

            if not fast_execution:
                print(f'TD target = R + 𝛾 * Q({s_prime}, {a_index_to_symbol[greedy_a]}) = '
                      f'{r:.2f} + 0.9 * {self.q_table[s_prime_idx, greedy_a]:.2f} = '
                      f'{td_target:.2f}')

            self.phase = 'computing_new_q_value'

        elif self.phase == 'computing_new_q_value':
            # Compute TD target
            s, a, r, s_prime, _ = self.current_transition
            s_idx = self.env.states.index(s)
            s_prime_idx = self.env.states.index(s_prime)
            greedy_a = np.random.choice(4, p=self.greedy_policy[self.s_idx])
            td_target = r + 0.9 * self.q_table[s_prime_idx, greedy_a]

            # Compute new value
            new_value = self.alpha * td_target + (1 - self.alpha) * self.q_table[s_idx, a]

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()

            if not fast_execution:
                print(f'TD target = {td_target:.2f}')
                print(f'Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * '
                      f'({td_target:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}')

            self.phase = 'showing_new_q_value'

        elif self.phase == 'showing_new_q_value':

            # Compute TD target
            s, a, r, s_prime, _ = self.current_transition
            s_idx = self.env.states.index(s)
            s_prime_idx = self.env.states.index(s_prime)
            greedy_a = np.random.choice(4, p=self.greedy_policy[self.s_idx])
            td_target = r + 0.9 * self.q_table[s_prime_idx, greedy_a]

            # Compute new value and update q-table
            new_value = self.alpha * td_target + (1 - self.alpha) * self.q_table[s_idx, a]
            self.q_table[s_idx, a] = new_value
            self.exploratory_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, self.epsilon)
            self.greedy_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, 0)

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()

                print(f'TD target = {td_target:.2f}')
                print(f'Q({s}, {a_index_to_symbol[a]}) = {new_value:.2f}')

            self.phase = 'choosing_actions'

        elif self.phase == 'update_q_value_terminal':
            s, a, r, s_prime, t = self.current_transition
            s_idx = self.env.states.index(s)
            new_value = self.alpha * r + (1-self.alpha)*self.q_table[s_idx, a]

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()

                print(f'Action sampled: {a_index_to_symbol[self.sampled_a]}\n')
                print('A terminal state has been reached: end of episode.\n')
                print(f'TD target = R + 𝛾 * 0 = {r:.2f}')
                print(f'Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * '
                      f'({r:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}')

            self.q_table[s_idx, a] = new_value
            self.exploratory_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, self.epsilon)
            self.greedy_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, 0)
            self.phase = 'showing_new_q_value_terminal'

        elif self.phase == 'showing_new_q_value_terminal':
            if not fast_execution:
                s, a, r, s_prime, t = self.current_transition
                s_idx = self.env.states.index(s)
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.greedy_policy, self.ax[2])
                plt.show()

                print(f'Action sampled: {a_index_to_symbol[self.sampled_a]}\n')
                print('A terminal state has been reached: end of episode.\n')
                print(f'TD target = R + 𝛾 * 0 = {r:.2f}')
                print(f'Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f}')

            self.current_transition = []
            self.env.reset()
            self.phase = 'choosing_actions'

        else:
            raise ValueError(f'Phase {self.phase} not recognized.')
        return print_string

    def finish_episode(self):
        print_string = ''
        while self.phase != 'showing_new_q_value_terminal':
            print_string += f'{self.next_step(fast_execution=True)}'
        print_string += f'{self.next_step(fast_execution=True)}'

        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
        plot_policy(self.env, self.greedy_policy, self.ax[2])
        plt.show()
        print(print_string)

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.exploratory_policy = epsilon_greedy_pi_from_q_table(self.env, self.q_table, self.epsilon)

        # Display plots
        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
        plot_policy(self.env, self.greedy_policy, self.ax[2])
        plt.show()
