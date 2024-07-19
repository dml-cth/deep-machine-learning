import matplotlib.pyplot as plt
import matplotlib

from lib.grid_world import a_index_to_symbol, get_pmf_possible_s_primes
from lib.plot_utils import plot_s_pmf, plot_policy, plot_value_table


class PolicyEvaluation:
    def __init__(self, env, policy, value_table):
        self.env = env
        self.policy = policy
        self.value_table = value_table

        self.fig, self.ax = None, None
        self.phase = "going_through_actions"
        self.i = 0
        self.s_i = 0
        self.a = 0
        self.q_values = [0, 0, 0, 0]
        self.q_messages = ""

        self.env.reset()

    @property
    def s(self):
        return self.env.states[self.s_i]

    def finish_iteration(self):
        initial_i = self.i
        while initial_i == self.i:
            self.next_step(fast_execution=True)

        # Plot the resulting state of the env, value table, and policy
        self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
        plot_s_pmf(self.env, self.s, self.a, ax=self.ax[0])
        plot_value_table(self.env, self.value_table, ax=self.ax[1], vmin=-8, vmax=0)
        plot_policy(self.env, self.policy, ax=self.ax[2])
        plt.show()

    def next_step(self, fast_execution=False):
        if not fast_execution:
            # Shared plotting for all phases
            self.fig, self.ax = plt.subplots(ncols=3, figsize=(20, 6))
            plot_s_pmf(self.env, self.s, self.a, ax=self.ax[0])
            plot_value_table(self.env, self.value_table, ax=self.ax[1], vmin=-8, vmax=0)
            plot_policy(self.env, self.policy, ax=self.ax[2])

            # Phase-specific plotting
            if (
                self.phase == "computing_final_v"
                and self.env.terminal_table[self.s_i] != 1
            ):
                self.ax[2].add_patch(
                    matplotlib.patches.Rectangle(
                        self.s, 1.0, 1.0, edgecolor="r", facecolor="None", lw=5
                    )
                )
            if self.phase == "updating_value_table":
                self.ax[1].add_patch(
                    matplotlib.patches.Rectangle(
                        self.s, 1.0, 1.0, edgecolor="r", facecolor="None", lw=5
                    )
                )
            plt.show()

            print(f"Iteration: {self.i}\nState: {self.s}\n")

        if self.phase == "going_through_actions":
            # Special handling for terminal states
            if self.env.terminal_table[self.s_i] == 1:
                self.a = 4
            else:
                # Get pmf over possible next states
                s_prime_idxs, s_prime_probs = get_pmf_possible_s_primes(
                    self.env, self.s, self.a
                )

                # Compute Q values
                q_message = f"Q(s, {a_index_to_symbol[self.a]}) = "
                r = self.env.reward_table[self.s_i, self.a]
                for s_prime_idx, s_prime_prob in zip(s_prime_idxs, s_prime_probs):
                    q_message += (
                        f"{s_prime_prob:.1f}*({r:.1f} + "
                        f"0.9*{self.value_table[s_prime_idx]:.2f}) + "
                    )
                    self.q_values[self.a] += s_prime_prob * (
                        r + 0.9 * self.value_table[s_prime_idx]
                    )

                # Prepare message to be printed
                q_message = q_message[:-2]
                q_message += f" = {self.q_values[self.a]:.2f}"
                self.q_messages += f"\n{q_message}"
                if not fast_execution:
                    print(self.q_messages)

                self.a += 1

            if self.a == 4:
                self.a = 3  # Show the same action as before
                self.phase = "computing_final_v"

        elif self.phase == "computing_final_v":
            if self.env.terminal_table[self.s_i] == 1:
                final_value_message = (
                    "State is terminal. Setting its value to zero.\nV(s) = 0"
                )
                if not fast_execution:
                    print(final_value_message)
                final_value = 0
            else:
                # Print computed Q messages
                if not fast_execution:
                    for i, q_value in enumerate(self.q_values):
                        print(f"Q(s, {a_index_to_symbol[i]}) = {q_value:.2f}")

                # Print resulting value of current state
                final_value_message = "\nV(s) = "
                final_value = 0
                for q_value, pi in zip(self.q_values, self.policy[self.s_i]):
                    final_value_message += f"{q_value:.2f}*{pi:.1f} + "
                    final_value += q_value * pi
                final_value_message = f"{final_value_message[:-3]}) = {final_value:.2f}"
                if not fast_execution:
                    print(final_value_message)

            # Update value table and move to next phase
            self.value_table[self.s_i] = final_value
            self.phase = "updating_value_table"

        elif self.phase == "updating_value_table":
            if not fast_execution:
                # Print computed Q messages
                for i, q_value in enumerate(self.q_values):
                    print(f"Q(s, {a_index_to_symbol[i]}) = {q_value:.2f}")

                # Print resulting value of current state
                print(f"\nV(s) = {self.value_table[self.s_i]:.2f}")

            # Reset action counter, move to next state, erase previous q messages
            self.a = 0
            self.s_i += 1
            self.q_messages = ""
            self.q_values = [0, 0, 0, 0]
            self.phase = "going_through_actions"

            # If reached last state, restart from first state and increment iteration number
            if self.s_i == len(self.env.states):
                self.s_i = 0
                self.i += 1


if __name__ == "__main__":
    from lib.grid_world import grid_world_3x3_stoch as env
    import numpy as np

    env.reset()
    value_table = np.zeros(9)
    policy = np.array(
        [
            [1, 0, 0, 0],
            [0.7, 0.3, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 0],
        ]
    )

    policy_eval = PolicyEvaluation(env, policy, value_table)
    for i in range(5):
        plt.close()
        policy_eval.next_step()
    policy_eval.finish_iteration()
