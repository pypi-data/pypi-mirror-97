import torch
import torch.nn as nn
import torch.nn.functional as F
import sve
from math import floor
from tqdm import tqdm
import numpy as np

device = 'cuda:0'

g = sve.N3Tree().to(device=device)
#  g.refine_at(0, (0,0,0))
#  #  g.refine_all()
#  g.refine_all()
