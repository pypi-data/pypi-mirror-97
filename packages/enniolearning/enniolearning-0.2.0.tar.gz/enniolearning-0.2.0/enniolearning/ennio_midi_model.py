from torch import nn
import torch
from enniolearning.utils import log

class ModelMidiLstm(nn.Module):

    # change input size for several tracks/instruments

    def __init__(self, n_vocab, input_size=1, lstm_hidden_cells_count=128, lstm_layer_count=3, **kwargs):
        super(ModelMidiLstm, self).__init__()

        self.lstm_layer_count = lstm_layer_count

        self.n_cells_lstm = input_size
        self.n_hidden_lstm = lstm_hidden_cells_count * input_size
        self.n_in_dense_1 = self.n_hidden_lstm
        self.n_out_dense_1 = int(self.n_in_dense_1 / 2)
        self.n_in_dense_2 = self.n_out_dense_1
        self.n_out_dense_2 = n_vocab * input_size

        self._init_modules()

        self.n_vocab = n_vocab
        self.output_size = input_size

        log(f'  Important parameters for Model construction (consider reducing these parameters if out of memory) :', **kwargs)
        log(f'    Depending on dataset (use ennio_pretraining.py to adjust) :', **kwargs)
        log(f'      - Instruments count (aka lstm_input_size) : {input_size}', **kwargs)
        log(f'      - n_vocab (all notes counts, including pitch, quarterLength, etc.) : {n_vocab}', **kwargs)
        log(f'    Free parameters before network instantiation (ModelMidiLstm init params) :', **kwargs)
        log(f'      - lstm_hidden_cells_count : {lstm_hidden_cells_count}', **kwargs)
        log(f'      - lstm_layer_count : {lstm_layer_count}', **kwargs)

    def _init_modules(self):
        """Initialize the modules."""
        # Project the input

        self.lstm = nn.LSTM(self.n_cells_lstm, self.n_hidden_lstm, num_layers=self.lstm_layer_count, batch_first=True,
                            dropout=0.3)
        #         self.lstm = nn.RNN(self.n_in_lstm, self.n_out_lstm, batch_first=True)
        self.bn1 = nn.BatchNorm1d(self.n_cells_lstm)
        self.dense1 = nn.Linear(self.n_in_dense_1, self.n_out_dense_1)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
        self.bn2 = nn.BatchNorm1d(self.n_out_dense_1)
        self.dense2 = nn.Linear(self.n_in_dense_2, self.n_out_dense_2)
        self.activation = nn.Softmax(dim=2)

    def forward(self, input_tensor):
        """Forward pass; map latent vectors to samples."""
        #         log(f"input. input shape = {input_tensor.shape}", level=logging.DEBUG, **kwargs) #torch.Size([32, 116, 23])
        #         log(f"previous state shape = {previous_state[0].shape}, {previous_state[1].shape}", level=logging.DEBUG, **kwargs)
        # previous_state = self.hidden
        # Dim1 = batch element. Dim2 = timesteps, timesequence, timestamp. Dim3 = feature, seq_len

        intermediate, (state_h, state_c) = self.lstm(input_tensor, self.hidden)
        # , previous_state) something needs to be fixed before passing the state --> how properly do it ?
        #         log(f"lstm state {state_h.shape} {state_c.shape}", level=logging.DEBUG, **kwargs) #both [3, 32, 256] (num_layers * num_directions, batch_size, lstm_hidden_cells_count)
        assert torch.equal(intermediate[:, -1, :], state_h[-1])
        #         intermediate = state[0][-1]
        intermediate = intermediate[:, -1, :]
        state_h = state_h.detach()
        state_c = state_c.detach()
        self.hidden = (state_h, state_c)
        #         log(f"lstm output shape = {intermediate.shape}", level=logging.DEBUG, **kwargs) #torch.Size([batch_size, self.n_hidden_lstm])

        #         intermediate = self.bn1(intermediate)

        intermediate = self.dropout(intermediate)

        intermediate = self.dense1(intermediate)
        #         log(f"linear/dense 1 output shape = {intermediate.shape}", level=logging.DEBUG, **kwargs) #torch.Size([8, 128])

        intermediate = self.relu(intermediate)

        #         intermediate = self.bn2(intermediate)

        intermediate = self.dropout(intermediate)

        intermediate = self.dense2(intermediate)
        #         log(f"linear/dense 2 output shape = {intermediate.shape}", level=logging.DEBUG, **kwargs) #torch.Size([batch_size, n_vocab*output_size])

        intermediate = intermediate.reshape(intermediate.shape[0], self.output_size, self.n_vocab)

        #         log(f"before activation = {intermediate.shape}", level=logging.DEBUG, **kwargs) #torch.Size([batch_size, output_size, n_vocab])

        output_tensor = self.activation(intermediate)
        return output_tensor

    def reinit_state(self, batch_size):
        return self.init_state(batch_size)

    def init_state(self, batch_size):
        if not batch_size:
            raise KeyError('batch_size is mandatory to init_state')
        weight = next(self.parameters())
        self.hidden = (weight.new_zeros(self.lstm_layer_count, batch_size, self.n_hidden_lstm),
                       weight.new_zeros(self.lstm_layer_count, batch_size, self.n_hidden_lstm))
#         self.hidden = (torch.zeros(self.lstm_layer_count, batch_size, self.n_hidden_lstm, dtype=torch.float32, device=device),
#                        torch.zeros(self.lstm_layer_count, batch_size, self.n_hidden_lstm, dtype=torch.float32, device=device))
