import numpy as np
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt

from lib.grid_world import grid_world_3x3_stoch as env
from lib.policy_evaluation_app import PolicyEvaluation


def policy_evaluation_wrapper():
    # Initial value table
    value_table = np.zeros(9)

    # Policy being evaluated
    policy = np.array([[1, 0, 0, 0], [0.5, 0.5, 0, 0], [0, 1, 0, 0],
                       [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]])

    btn = widgets.Button(description='Next step')
    btn_finish_iter = widgets.Button(description='Finish iteration')
    output = widgets.Output()

    env.reset()
    policy_eval = PolicyEvaluation(env, policy, value_table)

    def on_click_fn(obj):
        plt.close()
        output.clear_output(True)
        with output:
            policy_eval.next_step()

    def on_click_finish_iter_fn(obj):
        plt.close()
        output.clear_output(True)
        with output:
            policy_eval.finish_iteration()

    btn.on_click(on_click_fn)
    btn_finish_iter.on_click(on_click_finish_iter_fn)

    display(btn)
    display(btn_finish_iter)
    display(output)
