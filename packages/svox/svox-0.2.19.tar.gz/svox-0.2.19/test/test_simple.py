import torch
import torch.nn.functional as F
import svox

device='cuda:0'
t = svox.N3Tree(map_location=device)
