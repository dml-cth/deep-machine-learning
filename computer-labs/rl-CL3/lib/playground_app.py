import matplotlib.pyplot as plt

from lib.plot_utils import plot_all_states, plot_agent


class Playground:
    def __init__(self, env):
        self.env = env
        self.fig, self.ax = None, None
        self.current_episode_rewards = []
        self.env.reset()
        self.draw_env_and_agent()
        self.phase = "interacting"

    @property
    def s(self):
        return self.env.state

    @property
    def s_idx(self):
        return self.env.states.index(self.s)

    @property
    def s_centered(self):
        return [self.s[0] + 0.5, self.s[1] + 0.5]

    def draw_env_and_agent(self, old_s=None):
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        plot_all_states(self.env, self.ax)
        plot_agent(self.s, self.ax)
        if old_s is not None:
            plot_agent(old_s, self.ax, alpha=0.3)
        plt.show()

    def take_action(self, a):
        if self.phase == "interacting":
            old_s = self.s
            s_prime, r, t = self.env.step(a)
            self.current_episode_rewards.append(r)
            self.draw_env_and_agent(old_s=old_s)
            print("Rewards so far:")
            for i, r in enumerate(self.current_episode_rewards):
                print(f"r{i+1} = {r:.1f}, ", end="")
            print()
            if t:
                self.show_end_of_episode()

        elif self.phase == "cleaning_up":
            self.env.reset()
            self.current_episode_rewards = []

            self.draw_env_and_agent()
            print("Resetting environment.")

            self.phase = "interacting"

        else:
            raise ValueError(f"Phase {self.phase} not recognized. Quitting.")

    def show_end_of_episode(self):
        print("\nTerminal state reached, end of episode.")
        return_msg = ""
        g = 0
        for i, r in enumerate(self.current_episode_rewards):
            g += (0.9**i) * r
            return_msg += f"0.9^{i}*{r:.1f} "
            if i != len(self.current_episode_rewards) - 1:
                return_msg += "+ "
        print(f"Return for t=1: {return_msg} = {g:.2f}")

        self.phase = "cleaning_up"
