import torch
import svox
t = svox.N3Tree()

print(t._calc_corners(torch.tensor([[0, 0, 0, 0]])))
print(t._calc_corners(torch.tensor([[0, 1, 1, 1]])))
print(t._calc_corners(torch.tensor([[0, 2, 1, 2]])))

t.refine_all()
print(t._calc_corners(torch.tensor([[1, 2, 1, 2]])))
t.data[1,2,1,2] = 3.4
print(t(t._calc_corners(torch.tensor([[1, 2, 1, 2]]))))
