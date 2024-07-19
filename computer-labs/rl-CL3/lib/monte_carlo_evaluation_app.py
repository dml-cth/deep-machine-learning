import matplotlib.pyplot as plt
import numpy as np

from lib.plot_utils import (
    plot_all_states,
    plot_agent,
    plot_value_table,
    plot_env_agent_and_policy_at_state,
    plot_env_agent_and_chosen_action,
    plot_policy,
)
from lib.grid_world import a_index_to_symbol


class MonteCarloEvaluation:
    def __init__(self, env, policy, initial_value_table, alpha=0.1, vmin=-8, vmax=0.5):
        self.env = env
        self.policy = policy
        self.value_table = initial_value_table
        self.alpha = alpha
        self.vmin, self.vmax = vmin, vmax

        self.fig, self.ax = None, None
        self.phase = "choosing_actions"
        self.sampled_a = None
        self.current_episode = []
        self.current_episode_returns = []

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

    def get_current_episode_as_string(self):
        output_string = ""

        output_string += "Current episode:\n"
        for transition in self.current_episode:
            output_string += f"<{transition[0]}, {a_index_to_symbol[transition[1]]}, {transition[2]}, {transition[3]}>\n"

        return output_string

    def next_step(self, fast_execution=False):
        print_string = ""
        if self.phase == "choosing_actions":
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_policy_at_state(
                    self.env, self.s, self.policy, self.ax[0]
                )
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print("Sampling action...\n")
                print(self.get_current_episode_as_string())

            self.phase = "showing_sampled_action"

        elif self.phase == "showing_sampled_action":
            self.sampled_a = np.random.choice(4, p=self.policy[self.s_idx])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_env_agent_and_chosen_action(
                    self.env, self.s, self.sampled_a, self.ax[0]
                )
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(f"Action sampled: {a_index_to_symbol[self.sampled_a]}\n")
                print(self.get_current_episode_as_string())

            self.phase = "carrying_out_action"

        elif self.phase == "carrying_out_action":
            old_s = self.s
            s_prime, r, t = self.env.step(self.sampled_a)
            self.current_episode.append([old_s, self.sampled_a, r, s_prime])

            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(old_s, self.ax[0], alpha=0.3)
                plot_agent(self.s, self.ax[0])
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(self.get_current_episode_as_string())

            if t:
                if not fast_execution:
                    print("A terminal state has been reached: end of episode.")
                self.phase = "computing_returns"
            else:
                self.phase = "choosing_actions"

        elif self.phase == "computing_returns":
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(self.get_current_episode_as_string())
                print("\nComputing returns:")

            self.current_episode_returns = [0] * len(self.current_episode)
            for i in reversed(range(len(self.current_episode))):
                transition = self.current_episode[i]
                if i == len(self.current_episode) - 1:
                    if not fast_execution:
                        print(
                            f"G_{i+1} = {transition[2]:.1f},\t\t\t\tat {transition[0]}"
                        )
                    self.current_episode_returns[i] = transition[2]
                else:
                    self.current_episode_returns[i] = (
                        transition[2] + 0.9 * self.current_episode_returns[i + 1]
                    )
                    if not fast_execution:
                        print(
                            f"G_{i+1} = {transition[2]:.1f} + 0.9 * {self.current_episode_returns[i+1]:.2f}",
                            end="",
                        )
                        print(
                            f" = {self.current_episode_returns[i]:.2f},\tat {transition[0]}"
                        )

            self.phase = "presenting_computed_returns"

        elif self.phase == "presenting_computed_returns":
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(self.get_current_episode_as_string())

                print("\nComputing returns:")
                for i, (transition, g) in reversed(
                    list(
                        enumerate(
                            zip(self.current_episode, self.current_episode_returns)
                        )
                    )
                ):
                    print(f"G_{i+1} = {g:.2f},\tat {transition[0]}")

            self.phase = "updating_values"

        elif self.phase == "updating_values":
            if fast_execution:
                print_string += f"{self.get_current_episode_as_string()}\n"
            else:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(self.get_current_episode_as_string())
                print("\nComputing returns:")

            # Print computed returns for all visited states
            for i, (transition, g) in reversed(
                list(enumerate(zip(self.current_episode, self.current_episode_returns)))
            ):
                msg = f"G_{i+1} = {g:.2f},\tat {transition[0]}"
                if fast_execution:
                    print_string += f"{msg}\n"
                else:
                    print(msg)

            if fast_execution:
                print_string += "\n"
            else:
                print("\nUpdating values:")

            for transition, g in zip(
                reversed(self.current_episode), reversed(self.current_episode_returns)
            ):
                s_idx = self.env.states.index(transition[0])
                new_value = self.alpha * g + (1 - self.alpha) * self.value_table[s_idx]
                cur_value = self.value_table[s_idx]
                msg = (
                    f"V({transition[0]}) = {cur_value:.2f} + {self.alpha:.2f} * ({g:.2f} - {cur_value:.2f}) "
                    f"= {new_value:.2f}"
                )
                self.value_table[s_idx] = new_value
                if fast_execution:
                    print_string += f"{msg}\n"
                else:
                    print(msg)

            self.phase = "show_updated_value_function"

        elif self.phase == "show_updated_value_function":
            if not fast_execution:
                self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
                plot_all_states(self.env, self.ax[0])
                plot_agent(self.s, self.ax[0])
                plot_value_table(
                    self.env,
                    self.value_table,
                    self.ax[1],
                    vmin=self.vmin,
                    vmax=self.vmax,
                )
                plot_policy(self.env, self.policy, self.ax[2])
                plt.show()
                print(self.get_current_episode_as_string())

                print("\nComputing returns:")
                for i, (transition, g) in reversed(
                    list(
                        enumerate(
                            zip(self.current_episode, self.current_episode_returns)
                        )
                    )
                ):
                    print(f"G_{i+1} = {g:.2f},\tat {transition[0]}")

                print("\nUpdating values:")
                for transition, g in zip(
                    reversed(self.current_episode),
                    reversed(self.current_episode_returns),
                ):
                    s_idx = self.env.states.index(transition[0])
                    print(f"V({transition[0]}) = {self.value_table[s_idx]:.2f}")

            self.current_episode = []
            self.env.reset()
            self.phase = "choosing_actions"

        else:
            raise ValueError(f"Phase {self.phase} not recognized.")

        return print_string

    def finish_episode(self):
        print_string = ""
        while self.phase != "show_updated_value_function":
            print_string += f"{self.next_step(fast_execution=True)}"
        print_string += f"{self.next_step(fast_execution=True)}"

        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_all_states(self.env, self.ax[0])
        plot_agent(self.s, self.ax[0])
        plot_value_table(
            self.env, self.value_table, self.ax[1], vmin=self.vmin, vmax=self.vmax
        )
        plot_policy(self.env, self.policy, self.ax[2])
        plt.show()
        print(print_string)


if __name__ == "__main__":
    # def f():
    #     pass
    # plt.show = f

    from lib.grid_world import grid_world_3x3 as env

    policy = np.array(
        [
            [1, 0, 0, 0],
            [0.5, 0.5, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 0],
        ]
    )
    value_table = np.zeros(9)
    env.reset()
    mc_eval = MonteCarloEvaluation(env, policy, value_table)
    for i in range(1):
        mc_eval.next_step()
    mc_eval.finish_episode()
