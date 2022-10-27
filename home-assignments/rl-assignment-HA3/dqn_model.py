import torch
from torch import nn
import numpy as np
from collections import deque


class ExperienceReplay:
    def __init__(self, device, num_states, buffer_size=1e+6):
        self._device = device
        self.__buffer = deque(maxlen=int(buffer_size))
        self._num_states = num_states

    @property
    def buffer_length(self):
        return len(self.__buffer)

    def add(self, transition):
        '''
        Adds a transition <s, a, r, s', t > to the replay buffer
        :param transition:
        :return:
        '''
        self.__buffer.append(transition)

    def sample_minibatch(self, batch_size=128):
        '''
        :param batch_size:
        :return:
        '''
        ids = np.random.choice(a=self.buffer_length, size=batch_size)
        state_batch = np.zeros([batch_size, self._num_states],
                               dtype=np.float32)
        action_batch = np.zeros([
            batch_size,
        ], dtype=np.int64)
        reward_batch = np.zeros([
            batch_size,
        ], dtype=np.float32)
        nonterminal_batch = np.zeros([
            batch_size,
        ], dtype=np.bool)
        next_state_batch = np.zeros([batch_size, self._num_states],
                                    dtype=np.float32)
        for i, index in zip(range(batch_size), ids):
            state_batch[i, :] = self.__buffer[index].s
            action_batch[i] = self.__buffer[index].a
            reward_batch[i] = self.__buffer[index].r
            nonterminal_batch[i] = self.__buffer[index].t
            next_state_batch[i, :] = self.__buffer[index].next_s

        return (
            torch.tensor(state_batch, dtype=torch.float, device=self._device),
            torch.tensor(action_batch, dtype=torch.long, device=self._device),
            torch.tensor(reward_batch, dtype=torch.float, device=self._device),
            torch.tensor(next_state_batch,
                         dtype=torch.float,
                         device=self._device),
            torch.tensor(nonterminal_batch,
                         dtype=torch.bool,
                         device=self._device),
        )


class QNetwork(nn.Module):
    def __init__(self, num_states, num_actions):
        super().__init__()
        self._num_states = num_states
        self._num_actions = num_actions

        self._fc1 = nn.Linear(self._num_states, 100)
        self._relu1 = nn.ReLU(inplace=True)
        self._fc2 = nn.Linear(100, 60)
        self._relu2 = nn.ReLU(inplace=True)
        self._fc_final = nn.Linear(60, self._num_actions)

        # Initialize all bias parameters to 0, according to old Keras implementation
        nn.init.zeros_(self._fc1.bias)
        nn.init.zeros_(self._fc2.bias)
        nn.init.zeros_(self._fc_final.bias)
        # Initialize final layer uniformly in [-1e-6, 1e-6] range, according to old Keras implementation
        nn.init.uniform_(self._fc_final.weight, a=-1e-6, b=1e-6)

    def forward(self, state):
        h = self._relu1(self._fc1(state))
        h = self._relu2(self._fc2(h))
        q_values = self._fc_final(h)
        return q_values


class DeepQLearningModel(object):
    def __init__(self, device, num_states, num_actions, learning_rate):
        self._device = device
        self._num_states = num_states
        self._num_actions = num_actions
        self._lr = learning_rate

        # Define the two Q-networks
        self.online_model = QNetwork(self._num_states,
                                     self._num_actions).to(device=self._device)
        self.offline_model = QNetwork(
            self._num_states, self._num_actions).to(device=self._device)

        # Define optimizer. Should update online network parameters only.
        self.optimizer = torch.optim.RMSprop(self.online_model.parameters(),
                                             lr=self._lr)

        # Define loss function
        self._mse = nn.MSELoss(reduction='mean').to(device=self._device)

    def calc_loss(self, q_online_curr, q_target, a):
        '''
        Calculate loss for given batch
        :param q_online_curr: batch of q values at current state. Shape (N, num actions)
        :param q_target: batch of temporal difference targets. Shape (N,)
        :param a: batch of actions taken at current state. Shape (N,)
        :return:
        '''
        batch_size = q_online_curr.shape[0]
        assert q_online_curr.shape == (batch_size, self._num_actions)
        assert q_target.shape == (batch_size, )
        assert a.shape == (batch_size, )

        # Select only the Q-values corresponding to the actions taken (loss should only be applied for these)
        q_online_curr_allactions = q_online_curr
        q_online_curr = q_online_curr[torch.arange(batch_size),
                                      a]  # New shape: (batch_size,)
        assert q_online_curr.shape == (batch_size, )
        for j in [0, 3, 4]:
            assert q_online_curr_allactions[j, a[j]] == q_online_curr[j]

        # Make sure that gradient is not back-propagated through Q target
        assert not q_target.requires_grad

        loss = self._mse(q_online_curr, q_target)
        assert loss.shape == ()

        return loss

    def update_target_network(self):
        '''
        Update target network parameters, by copying from online network.
        '''
        online_params = self.online_model.state_dict()
        self.offline_model.load_state_dict(online_params)

def test_calculate_q_targets(calculate_q_targets_function):
    '''Tests an implementation of function that calculates Q targets

    : param calculate_q_targets_function: Func. specified in HA3.ipynb, Task 3

    Note: This does not test the behaviour with ambiguous q1_batches.
    '''

    # All zeros
    N = 10
    num_actions = 5
    q1_batch = torch.zeros((N, num_actions), dtype=torch.float32)
    r_batch = torch.zeros((N, ), dtype=torch.float32)
    nonterminal_batch = torch.zeros((N, ), dtype=torch.bool)
    gamma = 1

    true_targets = torch.zeros((N, ), dtype=torch.float32)

    calculated_targets = calculate_q_targets_function(q1_batch,
                                                      r_batch,
                                                      nonterminal_batch,
                                                      gamma)

    assert calculated_targets.size() == torch.Size(
        (N, )), "Failed: Incorrect size of Q tensor"

    sub_test_name = "All input zero"
    assert torch.allclose(
        calculated_targets, true_targets,
        rtol=1e-03), "Failed: Incorrect Q targets. Subtest: '{}'".format(
            sub_test_name)

    # Non-zero values
    # Gamma not 1
    sub_test_name = "Non-zero values, gamma not 1"
    N = 3
    num_actions = 2
    q1_batch = torch.tensor([[1, 0], [-2, -1], [0, 1]], dtype=torch.float32)
    r_batch = torch.ones((N, ), dtype=torch.float32)
    nonterminal_batch = torch.ones((N, ), dtype=torch.bool)
    gamma = 0.8

    true_targets = torch.tensor([1.8, 0.2, 1.8], dtype=torch.float32)

    calculated_targets = calculate_q_targets_function(q1_batch,
                                                      r_batch,
                                                      nonterminal_batch,
                                                      gamma)

    assert torch.allclose(
        calculated_targets, true_targets,
        rtol=1e-03), "Failed: Incorrect Q targets. Subtest: '{}'".format(
            sub_test_name)

    # Terminal state
    # Gamma not 1
    sub_test_name = "With terminal state"
    N = 3
    num_actions = 2
    q1_batch = torch.tensor([[1, 0], [-2, -1], [0, 1]], dtype=torch.float32)
    r_batch = torch.ones((N, ), dtype=torch.float32)
    nonterminal_batch = torch.tensor([False, True, True], dtype=torch.bool)
    gamma = 0.8

    true_targets = torch.tensor([1, 0.2, 1.8], dtype=torch.float32)

    calculated_targets = calculate_q_targets_function(q1_batch,
                                                      r_batch,
                                                      nonterminal_batch,
                                                      gamma)

    assert torch.allclose(
        calculated_targets, true_targets,
        rtol=1e-03), "Failed: Incorrect Q targets. Subtest: '{}'".format(
            sub_test_name)

    sub_test_name = "Single action"
    N = 2
    gamma = 1
    q1_batch = torch.tensor([[1], [2]], dtype=torch.float32)
    r_batch = torch.ones((N, ), dtype=torch.float32)
    nonterminal_batch = torch.ones((N, ), dtype=torch.bool)
    num_actions = 1

    true_targets = torch.tensor([2, 3], dtype=torch.float32)

    calculated_targets = calculate_q_targets_function(q1_batch,
                                                      r_batch,
                                                      nonterminal_batch,
                                                      gamma)
                                               
    assert torch.allclose(
        calculated_targets, true_targets,
        rtol=1e-03), "Failed: Incorrect Q targets. Subtest: '{}'".format(
            sub_test_name)

    print('Passed: Calculate Q targets test, for function "{}"'.format(
        calculate_q_targets_function.__name__))