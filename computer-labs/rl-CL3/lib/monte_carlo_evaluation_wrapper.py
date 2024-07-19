import numpy as np
from lib.grid_world import grid_world_3x3 as env
from lib.monte_carlo_evaluation_app import MonteCarloEvaluation

import ipywidgets as widgets
from IPython.display import display

import matplotlib.pyplot as plt


def monte_carlo_evaluation_wrapper():
    env.reset()
    value_table = np.zeros(9)
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

    btn = widgets.Button(description="Next step")
    finish_episode_btn = widgets.Button(description="Finish episode")
    output = widgets.Output()

    mc_eval = MonteCarloEvaluation(env, policy, value_table)

    def on_click_fn(obj):
        plt.close()
        output.clear_output(True)

        with output:
            mc_eval.next_step()

    def on_click_finish_episode_fn(obj):
        plt.close()
        output.clear_output(True)
        with output:
            mc_eval.finish_episode()

    btn.on_click(on_click_fn)
    finish_episode_btn.on_click(on_click_finish_episode_fn)
    display(btn)
    display(finish_episode_btn)
    display(output)
