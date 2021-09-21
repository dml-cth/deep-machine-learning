import ipywidgets as widgets

from IPython.display import display
import matplotlib.pyplot as plt


from lib.playground_app import Playground


def playground_wrapper(env):
    btn_up = widgets.Button(description='↑', layout=widgets.Layout(width='10%', height='50px'))
    btn_right = widgets.Button(description='→', layout=widgets.Layout(width='10%', height='50px'))
    btn_down = widgets.Button(description='↓', layout=widgets.Layout(width='10%', height='50px'))
    btn_left = widgets.Button(description='←', layout=widgets.Layout(width='10%', height='50px'))
    hbox = widgets.HBox([btn_up, btn_right, btn_down, btn_left])
    output = widgets.Output()
    env.reset()
    with output:
        playground = Playground(env)

    def create_move_fn(action):
        def move_up(obj):
            plt.close()
            output.clear_output(True)
            with output:
                playground.take_action(action)
        return move_up

    btn_up.on_click(create_move_fn(0))
    btn_right.on_click(create_move_fn(1))
    btn_down.on_click(create_move_fn(2))
    btn_left.on_click(create_move_fn(3))
    display(hbox)
    display(output)
