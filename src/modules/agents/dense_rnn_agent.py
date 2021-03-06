import torch as th
import torch.nn as nn
import torch.nn.functional as F


class DenseRNNAgent(nn.Module):
    def __init__(self, input_shape, args):
        super(DenseRNNAgent, self).__init__()
        self.args = args

        self.fc1 = nn.Linear(input_shape, args.dense_size)
        self.fc2 = nn.Linear(args.dense_size, args.dense_size)
        self.rnn3 = nn.GRUCell(args.dense_size, args.dense_size)
        self.fc4 = nn.Linear(args.dense_size, args.n_actions)

    def init_hidden(self):
        # make hidden states on same device as model
        return self.fc1.weight.new(1, self.args.dense_size).zero_()

    def forward(self, inputs, hidden_state):

        x1 = F.relu(self.fc1(inputs))
        x2 = F.relu(self.fc2(x1))

        h_in = hidden_state.reshape(-1, self.args.dense_size)
        h = self.rnn3(x2, h_in)

        q = self.fc4(h)

        return q, h
