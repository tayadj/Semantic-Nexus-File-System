import torch



class Summarifier(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()



class PositionalEncoder(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.dimension = config.get("dimension", 32)
		self.sequence_length = config.get("sequence_length", 128)
		self.dropout_rate = config.get("dropout_rate", 0.1)
		
		self.dropout = torch.nn.Dropout(p = self.dropout_rate)
		
		encoder = torch.zeros(self.sequence_length, self.dimension)
		position = torch.arange(self.sequence_length).unsqueeze(1).float()
		term = torch.exp(torch.arange(0, self.dimension, 2).float() * (-torch.log(torch.tensor(10000.0)) / self.dimension))
		encoder[:, 0::2] = torch.sin(position * term)
		encoder[:, 1::2] = torch.cos(position * term)
		encoder = encoder.unsqueeze(0)

		self.register_buffer("encoder", encoder)

	def forward(self, x: torch.Tensor) -> torch.Tensor:

		x = x + self.encoder[:, :x.size(1), :]
		x = self.dropout(x)

		return x