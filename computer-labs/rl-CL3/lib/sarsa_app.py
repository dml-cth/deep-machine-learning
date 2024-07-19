import matplotlib.pyplot as plt
import numpy as np

from lib.algos import epsilon_greedy_pi_from_q_table
from lib.plot_utils import (
    plot_all_states,
    plot_agent,
    plot_q_table,
    plot_env_agent_and_policy_at_state,
    plot_env_agent_and_chosen_action,
    plot_policy,
)
from lib.grid_world import a_index_to_symbol


class SarsaApp:
    def __init__(self, env, initial_q_table, alpha=0.2, vmin=-8, vmax=0.5):
        self.env = env
        self.q_table = initial_q_table
        self.alpha = alpha
        self.epsilon = 1.0
        self.vmin, self.vmax = vmin, vmax

        self.fig, self.ax = None, None
        self.phase = "initial_sampling_action"
        self.sampled_a = None
        self.current_transition = []
        self.i = 0
        self.policy = epsilon_greedy_pi_from_q_table(
            self.env, self.q_table, self.epsilon
        )

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
        print_string = ""
        if self.phase == "initial_sampling_action":
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_policy_at_state(
                    self.env, self.s, self.policy, self.ax[0]
                )
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print("Sampling action...\n")

            self.phase = "initial_showing_sampled_action"

        elif self.phase == "initial_showing_sampled_action":
            self.sampled_a = np.random.choice(4, p=self.policy[self.s_idx])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f"Action sampled: {a_index_to_symbol[self.sampled_a]}\n")

            self.phase = "carrying_out_action"

        elif self.phase == "carrying_out_action":
            old_s = self.s
            s_prime, r, t = self.env.step(self.sampled_a)
            self.current_transition = [old_s, self.sampled_a, r, s_prime, t]

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_agent(self.s, self.ax[0])
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f"Action sampled: {a_index_to_symbol[self.sampled_a]}\n")

            if not t:
                self.phase = "sampling_action"
            else:
                self.phase = "compute_q_for_terminal_s_prime"

        elif self.phase == "sampling_action":
            if not fast_execution:
                old_s = self.current_transition[0]
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_policy_at_state(
                    self.env, self.s, self.policy, self.ax[0]
                )
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print("Sampling action...\n")

            self.phase = "showing_sampled_action"

        elif self.phase == "showing_sampled_action":
            self.sampled_a = np.random.choice(4, p=self.policy[self.s_idx])
            self.current_transition.append(self.sampled_a)

            if not fast_execution:
                old_s = self.current_transition[0]
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f"Action sampled: {a_index_to_symbol[self.sampled_a]}\n")

            self.phase = "showing_transition_done"

        elif self.phase == "showing_transition_done":
            if not fast_execution:
                old_s = self.current_transition[0]
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

                s, a, r, s_prime, t, a_prime = self.current_transition
                print(
                    f"Transition: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, {a_index_to_symbol[a_prime]}>\n"
                )

            self.phase = "showing_td_target"

        elif self.phase == "showing_td_target":
            if not fast_execution:
                s, a, r, s_prime, t, a_prime = self.current_transition
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

                print(
                    f"Transition: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, {a_index_to_symbol[a_prime]}>\n"
                )

                s_prime_idx = self.env.states.index(s_prime)
                td_target = r + 0.9 * self.q_table[s_prime_idx, a_prime]
                print(
                    f"TD target: R + 𝛾 * Q({s_prime}, {a_index_to_symbol[a_prime]}) = "
                    f"{r:.2f} + 0.9 * {self.q_table[s_prime_idx, a_prime]:.2f} = "
                    f"{td_target:.2f}"
                )

            self.phase = "show_q_value_computation"

        elif self.phase == "show_q_value_computation":
            s, a, r, s_prime, t, a_prime = self.current_transition
            if not fast_execution:
                plot_agent(s, self.ax[0], alpha=0.3)
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

            s_idx = self.env.states.index(s)
            s_prime_idx = self.env.states.index(s_prime)
            td_target = r + 0.9 * self.q_table[s_prime_idx, a_prime]
            new_value = (
                self.alpha * td_target + (1 - self.alpha) * self.q_table[s_idx, a]
            )

            if fast_execution:
                msg = (
                    f"Transition: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, {a_index_to_symbol[a_prime]}>\n"
                    f"TD target: R + 𝛾 * Q({s_prime}, {a_index_to_symbol[a_prime]}) = "
                    f"{r:.2f} + 0.9 * {self.q_table[s_prime_idx, a_prime]:.2f} = {td_target:.2f}\n"
                    f"Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * "
                    f"({td_target:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}\n\n"
                )
                print_string += msg
            else:
                print(
                    f"Transition: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, {a_index_to_symbol[a_prime]}>\n"
                )
                print(f"TD target: {td_target:.2f}")
                print(
                    f"Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * "
                    f"({td_target:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}"
                )

            self.q_table[s_idx, a] = new_value
            self.policy = epsilon_greedy_pi_from_q_table(
                self.env, self.q_table, self.epsilon
            )

            self.phase = "showing_updated_q_value"

        elif self.phase == "showing_updated_q_value":
            if not fast_execution:
                s, a, r, s_prime, t, a_prime = self.current_transition
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

                print(
                    f"Transition: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, {a_index_to_symbol[a_prime]}>\n"
                )

                s_prime_idx = self.env.states.index(s_prime)
                td_target = r + 0.9 * self.q_table[s_prime_idx, a_prime]
                print(f"TD target: {td_target:.2f}")

                s_idx = self.env.states.index(s)
                print(f"Q({s, a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f}")

            self.phase = "carrying_out_action"

        elif self.phase == "compute_q_for_terminal_s_prime":
            s, a, r, s_prime, t = self.current_transition
            s_idx = self.env.states.index(s)
            new_value = self.alpha * r + (1 - self.alpha) * self.q_table[s_idx, a]

            if fast_execution:
                print_string += f"Transition to terminal state: <{s}, {a_index_to_symbol[a]}, {r:.1f}, {s_prime}, ∅>\n"
                print_string += f"TD target = R + 𝛾 * 0 = {r:.2f}\n"
                print_string += (
                    f"Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * "
                    f"({r:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}"
                )

            else:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_agent(s_prime, self.ax[0])
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print("Terminal state reached.\n")
                print(f"TD target = R + 𝛾 * 0 = {r:.2f}")
                print(
                    f"Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f} + {self.alpha:.2f} * "
                    f"({r:.2f} - {self.q_table[s_idx, a]:.2f}) = {new_value:.2f}"
                )

            self.q_table[s_idx, a] = new_value
            self.policy = epsilon_greedy_pi_from_q_table(
                self.env, self.q_table, self.epsilon
            )

            self.phase = "showing_updated_q_value_terminal_s_prime"

        elif self.phase == "showing_updated_q_value_terminal_s_prime":
            self.env.reset()
            self.i += 1

            if not fast_execution:
                s, a, r, s_prime, t = self.current_transition
                s_idx = self.env.states.index(s)

                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(s, self.ax[0], alpha=0.3)
                plot_agent(s_prime, self.ax[0])
                plot_q_table(
                    self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()

                print("Terminal state reached.\n")
                print(
                    f"Q({s}, {a_index_to_symbol[a]}) = {self.q_table[s_idx, a]:.2f}\n"
                )
                print("Resetting environment")

            self.phase = "initial_sampling_action"

        else:
            raise ValueError(f"Phase {self.phase} not recognized.")
        return print_string

    def finish_episode(self):
        print_string = ""
        current_i = self.i
        while self.i == current_i:
            print_string += f"{self.next_step(fast_execution=True)}"

        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
        plot_policy(self.env, self.policy, self.ax[2])
        plt.show()
        print(print_string)

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.policy = epsilon_greedy_pi_from_q_table(
            self.env, self.q_table, self.epsilon
        )

        # Display plots
        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_q_table(self.env, self.q_table, self.ax[1], vmin=self.vmin, vmax=self.vmax)
        plot_policy(self.env, self.policy, self.ax[2])
        plt.show()


if __name__ == "__main__":
    from lib.grid_world import grid_world_2x2 as env

    env.reset()
    initial_q_table = np.zeros((len(env.states), 4))
    sarsa = SarsaApp(env, initial_q_table)
    for i in range(1):
        sarsa.next_step()
    sarsa.finish_episode()
