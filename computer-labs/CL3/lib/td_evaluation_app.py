import matplotlib.pyplot as plt
import numpy as np

from lib.plot_utils import plot_all_states, plot_agent, plot_value_table, plot_env_agent_and_policy_at_state, \
    plot_env_agent_and_chosen_action, plot_policy
from lib.grid_world import a_index_to_symbol


class TDEvaluation:
    def __init__(self, env, policy, initial_value_table, alpha=0.2, vmin=-8, vmax=0.5):
        self.env = env
        self.policy = policy
        self.value_table = initial_value_table
        self.alpha = alpha
        self.vmin, self.vmax = vmin, vmax

        self.fig, self.ax = None, None
        self.phase = 'choosing_actions'
        self.sampled_a = None
        self.current_episode = []
        self.current_episode_returns = []
        self.i = 0

        self.td_target = None

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
                plot_env_agent_and_policy_at_state(self.env, self.s, self.policy, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print('Sampling action...\n')

            self.phase = 'showing_sampled_action'

        elif self.phase == 'showing_sampled_action':
            self.sampled_a = np.random.choice(4, p=self.policy[self.s_idx])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(self.env, self.s, self.sampled_a, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f'Action sampled: {a_index_to_symbol[self.sampled_a]}\n')

            self.phase = 'carrying_out_action'

        elif self.phase == 'carrying_out_action':
            old_s = self.s
            s_prime, r, t = self.env.step(self.sampled_a)
            self.current_episode.append([old_s, self.sampled_a, r, s_prime, t])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_agent(self.s, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f'Transition: <{old_s}, {a_index_to_symbol[self.sampled_a]}, {r:.1f}, {s_prime}>')

            self.phase = 'showing_td_target'

        elif self.phase == 'showing_td_target':
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

            old_s, a, r, s_prime, _ = self.current_episode[-1]
            s_prime_idx = self.env.states.index(s_prime)
            self.td_target = r + 0.9 * self.value_table[s_prime_idx]
            if not fast_execution:
                print(f'Transition: <{old_s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}>\n')
                print('Updating value table:')
                print(f'TD target = R + 𝛾 * V({s_prime}) = {r:.1f} + 0.9*{self.value_table[s_prime_idx]:.2f} = '
                      f'{self.td_target:.2f}')

            self.phase = 'updating_value_table'

        elif self.phase == 'updating_value_table':
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

            old_s, a, r, s_prime, _ = self.current_episode[-1]
            old_s_idx = self.env.states.index(old_s)
            new_value = self.alpha * self.td_target + (1 - self.alpha) * self.value_table[old_s_idx]

            if fast_execution:
                print_string += f'Transition: <{old_s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}>\n'
                print_string += f'TD target = {self.td_target:.2f}\n'
                print_string += f'V({old_s}) ← {self.value_table[old_s_idx]:.2f} + {self.alpha:.2f} * ' \
                                f'({self.td_target:.2f} - {self.value_table[old_s_idx]:.2f}) = {new_value:.2f}\n\n'
            else:
                print(f'Transition: <{old_s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}>\n')
                print('Updating value table:')
                print(f'TD target = {self.td_target:.2f}')
                print(f'V({old_s}) ← {self.value_table[old_s_idx]:.2f} + {self.alpha:.2f} * '
                      f'({self.td_target:.2f} - {self.value_table[old_s_idx]:.2f}) = {new_value:.2f}\n')

            self.value_table[old_s_idx] = new_value
            self.phase = 'showing_new_value_table'

        elif self.phase == 'showing_new_value_table':
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

            old_s, a, r, s_prime, t = self.current_episode[-1]
            old_s_idx = self.env.states.index(old_s)

            if not fast_execution:
                print(f'Transition: <{old_s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}>\n')
                print('Updating value table:')
                print(f'TD target = {self.td_target:.2f}')
                print(f'V({old_s}) = {self.value_table[old_s_idx]:.2f}')

            if t:
                if not fast_execution:
                    print('\nTerminal state, reseting environment.')
                self.env.reset()
                self.current_episode = []
                self.i += 1
            self.phase = 'choosing_actions'

        else:
            raise ValueError(f'Phase {self.phase} not recognized.')
        return print_string

    def finish_episode(self):
        print_string = ''
        current_i = self.i
        while self.i == current_i:
            print_string += f'{self.next_step(fast_execution=True)}'

        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_value_table(self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
        plot_policy(self.env, self.policy, self.ax[2])
        plt.show()
        print(print_string)
