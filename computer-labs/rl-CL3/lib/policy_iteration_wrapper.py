import numpy as np
from lib.grid_world import grid_world_3x3_stoch as env
from lib.plot_utils import plot_value_table, plot_policy
from lib.algos import policy_evaluation_one_step, policy_improvement

import ipywidgets as widgets
from IPython.display import display

import matplotlib.pyplot as plt


def policy_iteration_wrapper():
    env.reset()
    value_table = np.zeros(9)
    policy = np.array([[1, 0, 0, 0], [0.5, 0.5, 0, 0], [0, 1, 0, 0],
                       [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]])

    btn_eval = widgets.Button(description='Policy eval iteration')
    btn_improve = widgets.Button(description='Policy improvement')

    display(btn_eval)
    display(btn_improve)

    output = widgets.Output()

    vmin = -8
    vmax = 0
    with output:
        fig, ax = plt.subplots(ncols=2, figsize=(14, 6))
        plot_value_table(env, value_table, ax=ax[0], vmin=vmin, vmax=vmax)
        plot_policy(env, policy, ax=ax[1])
        plt.show()

    def policy_eval_on_click(obj):
        plt.close()
        fig, ax = plt.subplots(ncols=2, figsize=(14, 6))
        output.clear_output(True)
        policy_evaluation_one_step(env, policy, value_table)
        with output:
            plot_value_table(env, value_table, ax=ax[0], vmin=vmin, vmax=vmax)
            plot_policy(env, policy, ax=ax[1])
            plt.show()

    def policy_improve_on_click(obj):
        plt.close()
        fig, ax = plt.subplots(ncols=2, figsize=(14, 6))
        output.clear_output(True)
        policy_improvement(env, policy, value_table)
        with output:
            plot_value_table(env, value_table, ax=ax[0], vmin=vmin, vmax=vmax)
            plot_policy(env, policy, ax=ax[1])
            plt.show()

    btn_eval.on_click(policy_eval_on_click)
    btn_improve.on_click(policy_improve_on_click)
    display(output)
