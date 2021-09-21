import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

from lib.grid_world import get_pmf_possible_s_primes


def plot_value_table(env, value_table, ax=None, vmin=None, vmax=None):
    if vmin is None:
        vmin = min(value_table)
    if vmax is None:
        vmax = max(value_table)

    plasma = plt.get_cmap('plasma')
    cNorm = colors.Normalize(vmin=vmin, vmax=vmax)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=plasma)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    for s in env.states:
        value = value_table[env.states.index(s)]
        ax.add_patch(matplotlib.patches.Rectangle(s, 1, 1, edgecolor='k', facecolor=scalarMap.to_rgba(value)))
        ax.annotate(f'{value:.2f}', [s[0]+0.5, s[1]+0.5], c='k', fontsize=15, ha='center', va='center')

    ax.axis('off')
    ax.relim()
    ax.autoscale_view()
    ax.set_title('Value table')


def plot_q_table(env, q_table, ax=None, vmin=None, vmax=None):
    if vmin is None:
        vmin = min(q_table.flatten())
    if vmax is None:
        vmax = max(q_table.flatten())

    plasma = plt.get_cmap('plasma')
    cNorm = colors.Normalize(vmin=vmin, vmax=vmax)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=plasma)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    for s_i, s in enumerate(env.states):
        s_centered = [s[0]+0.5, s[1]+0.5]
        s_upper_left = [s[0], s[1]+1]
        s_upper_right = [s[0]+1, s[1]+1]
        s_bottom_right = [s[0]+1, s[1]]

        ax.add_patch(matplotlib.patches.Polygon([s_upper_left, s_centered, s_upper_right], edgecolor='k',
                                                facecolor=scalarMap.to_rgba(q_table[s_i, 0])))
        ax.add_patch(matplotlib.patches.Polygon([s_upper_right, s_centered, s_bottom_right], edgecolor='k',
                                                facecolor=scalarMap.to_rgba(q_table[s_i, 1])))
        ax.add_patch(matplotlib.patches.Polygon([s, s_centered, s_bottom_right], edgecolor='k',
                                                facecolor=scalarMap.to_rgba(q_table[s_i, 2])))
        ax.add_patch(matplotlib.patches.Polygon([s, s_centered, s_upper_left], edgecolor='k',
                                                facecolor=scalarMap.to_rgba(q_table[s_i, 3])))

        ax.annotate(f'{q_table[s_i, 0]:.2f}', [s_centered[0], s_centered[1]+0.3], c='k', fontsize=12, ha='center', va='center')
        ax.annotate(f'{q_table[s_i, 1]:.2f}', [s_centered[0]+0.3, s_centered[1]], c='k', fontsize=12, ha='center', va='center')
        ax.annotate(f'{q_table[s_i, 2]:.2f}', [s_centered[0], s_centered[1]-0.3], c='k', fontsize=12, ha='center', va='center')
        ax.annotate(f'{q_table[s_i, 3]:.2f}', [s_centered[0]-0.3, s_centered[1]], c='k', fontsize=12, ha='center', va='center')

    ax.axis('off')
    ax.relim()
    ax.autoscale_view()
    ax.set_title('Q-value table')


def plot_policy(env, policy, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    for s_idx, s in enumerate(env.states):
        ax.add_patch(matplotlib.patches.Rectangle(s, 1, 1, edgecolor='k', facecolor='w'))

        s_centered = [s[0] + 0.5, s[1] + 0.5]
        delta = 0.3
        # Plot policy up
        ax.annotate(f'{policy[s_idx, 0]:.1f}'.lstrip('0'), [s_centered[0], s_centered[1]+delta], c='k', fontsize=15, ha='center', va='center')

        # Plot policy right
        ax.annotate(f'{policy[s_idx, 1]:.1f}'.lstrip('0'), [s_centered[0]+delta, s_centered[1]], c='k', fontsize=15, ha='center', va='center')

        # Plot policy down
        ax.annotate(f'{policy[s_idx, 2]:.1f}'.lstrip('0'), [s_centered[0], s_centered[1]-delta], c='k', fontsize=15, ha='center', va='center')

        # Plot policy left
        ax.annotate(f'{policy[s_idx, 3]:.1f}'.lstrip('0'), [s_centered[0]-delta, s_centered[1]], c='k', fontsize=15, ha='center', va='center')

        ax.arrow(s_centered[0], s_centered[1], delta / 2, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none', alpha=policy[s_idx, 1])
        ax.arrow(s_centered[0], s_centered[1], -delta / 2, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none', alpha=policy[s_idx, 3])
        ax.arrow(s_centered[0], s_centered[1], 0.0, delta / 2, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none', alpha=policy[s_idx, 0])
        ax.arrow(s_centered[0], s_centered[1], 0.0, -delta / 2, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none', alpha=policy[s_idx, 2])

        ax.relim()
        ax.autoscale_view()

    ax.axis('off')
    ax.set_title('Policy table')


def plot_s_pmf(env, s, a, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    plasma = plt.get_cmap('binary')
    cNorm = colors.Normalize(vmin=-0.1, vmax=1.3)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=plasma)

    # Draw all states
    for s_ in env.states:
        ax.add_patch(matplotlib.patches.Rectangle(s_, 1, 1, edgecolor='k', facecolor='w'))
    ax.axis('off')
    ax.relim()
    ax.autoscale_view()
    
    # Special handling for terminal states
    if env.terminal_table[env.states.index(s)] == 1:
        ax.add_patch(matplotlib.patches.Rectangle(s, 1, 1, edgecolor='k', facecolor='gray'))
        ax.annotate('Terminal', [s[0]+0.5, s[1]+0.5], c='k', fontsize=15, ha='center', va='center')
        return [env.states.index(s)], [1.0]

    # Add text representing next states pmf
    s_prime_idxs, s_pmf = get_pmf_possible_s_primes(env, s, a)
    for s_prime_idx, prob in zip(s_prime_idxs, s_pmf):
        s_prime = env.states[s_prime_idx]
        s_prime_centered = [s_prime[0] + 0.5, s_prime[1] + 0.5]

        # Add text showing probability and coloring
        ax.annotate(f'{prob:.1f}'.lstrip('0'), s_prime_centered, c='k', fontsize=15, ha='center', va='center')
        ax.add_patch(matplotlib.patches.Rectangle(s_prime, 1, 1, edgecolor='k', facecolor=scalarMap.to_rgba(prob)))

    s_centered = [s[0] + 0.5, s[1] + 0.5]
    # Draw arrow corresponding to intended direction
    if a == 0:
        ax.arrow(s_centered[0], s_centered[1]+0.25, 0.0, 0.5, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    elif a == 1:
        ax.arrow(s_centered[0]+0.25, s_centered[1], 0.5, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    elif a == 2:
        ax.arrow(s_centered[0], s_centered[1]-0.25, 0.0, -0.5, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    elif a == 3:
        ax.arrow(s_centered[0]-0.25, s_centered[1], -0.5, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')

    ax.set_title('Probability mass function for s\'')


def plot_all_states(env, ax):
    # Draw all states
    for i, s_ in enumerate(env.states):
        facecolor = 'tab:gray' if env.terminal_table[i] else 'w'
        ax.add_patch(matplotlib.patches.Rectangle(s_, 1, 1, edgecolor='k', facecolor=facecolor))
    ax.axis('off')
    ax.relim()
    ax.autoscale_view()


def plot_all_states_with_indices(env, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    # Draw all states
    for i, s_ in enumerate(env.states):
        facecolor = 'tab:gray' if env.terminal_table[i] else 'w'
        ax.add_patch(matplotlib.patches.Rectangle(s_, 1, 1, edgecolor='k', facecolor=facecolor))
        ax.annotate(f'({s_[0]}, {s_[1]})', [s_[0]+0.5, s_[1]+0.5], c='k', fontsize=15, ha='center', va='center')
    ax.axis('off')
    ax.relim()
    ax.autoscale_view()


def plot_agent(s, ax, alpha=1.0):
    s_centered = [s[0] + 0.5, s[1] + 0.5]
    ax.add_patch(matplotlib.patches.Circle(s_centered, 0.08, edgecolor='k', facecolor='k', alpha=alpha))


def plot_env_agent_and_policy_at_state(env, s, policy, ax):
    plot_all_states(env, ax)
    plot_agent(s, ax)
    s_idx = env.states.index(s)
    s_centered = [s[0] + 0.5, s[1] + 0.5]

    # Plot policy probabilities
    delta_text = 0.3
    ax.annotate(f'{policy[s_idx, 0]:.1f}'.lstrip('0'), [s_centered[0], s_centered[1] + delta_text], c='k', fontsize=15, ha='center', va='center')
    ax.annotate(f'{policy[s_idx, 1]:.1f}'.lstrip('0'), [s_centered[0] + delta_text, s_centered[1]], c='k', fontsize=15, ha='center', va='center')
    ax.annotate(f'{policy[s_idx, 2]:.1f}'.lstrip('0'), [s_centered[0], s_centered[1] - delta_text], c='k', fontsize=15, ha='center', va='center')
    ax.annotate(f'{policy[s_idx, 3]:.1f}'.lstrip('0'), [s_centered[0] - delta_text, s_centered[1]], c='k', fontsize=15, ha='center', va='center')

    # Plot arrows
    delta_arrow = 0.5
    ax.arrow(s_centered[0], s_centered[1], delta_arrow / 2, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    ax.arrow(s_centered[0], s_centered[1], -delta_arrow / 2, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    ax.arrow(s_centered[0], s_centered[1], 0.0, delta_arrow / 2, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')
    ax.arrow(s_centered[0], s_centered[1], 0.0, -delta_arrow / 2, length_includes_head=True, width=0.01, head_width=0.1, facecolor='k', edgecolor='none')


def plot_env_agent_and_chosen_action(env, s, a, ax):
    plot_all_states(env, ax)
    plot_agent(s, ax)
    s_centered = [s[0] + 0.5, s[1] + 0.5]
    if a == 0:
        ax.arrow(s_centered[0], s_centered[1], 0.0, 0.4, length_includes_head=True, width=0.01, head_width=0.1, facecolor='g', edgecolor='none')
    elif a == 1:
        ax.arrow(s_centered[0], s_centered[1], 0.4, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='g', edgecolor='none')
    elif a == 2:
        ax.arrow(s_centered[0], s_centered[1], 0.0, -0.4, length_includes_head=True, width=0.01, head_width=0.1, facecolor='g', edgecolor='none')
    elif a == 3:
        ax.arrow(s_centered[0], s_centered[1], -0.4, 0.0, length_includes_head=True, width=0.01, head_width=0.1, facecolor='g', edgecolor='none')
    else:
        raise ValueError(f'Cannot plot action {a}. Action should be in [0,3].')


if __name__ == '__main__':
    from lib.grid_world import grid_world_3x3 as env
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    plot_all_states(env, ax, plot_indexes=True)
    plt.show()
