import torch
import torch.nn.functional as F
import svox
from tqdm import tqdm

device = 'cuda:0'
torch.cuda.set_device(device)
#  device = 'cpu'
torch.random.manual_seed(1234)
N = 64
K = 4
g = svox.N3Tree(N=K, map_location=device).to(device=device)

q = torch.rand((1, 3), device=device)
print('begin refine')
for j in tqdm(range(10)):
    q = torch.rand((100, 3), device=device)
    g[q].refine()
    for i in range(20):
        q = torch.rand((3, 3), device=device)
        vals = 100 * torch.randn((3, K), device=device)
        g.set(q, vals)
#
q = torch.rand((100000, 3), device=device)

# -------------

r_nc = g(q, cuda=False)
sm_nc = r_nc.sum()

start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
torch.cuda.synchronize()
start.record()

sm_nc.backward()

end.record()
torch.cuda.synchronize()
print('time', start.elapsed_time(end), 'ms')

grad2 = g.data.grad.clone()
print(grad2.shape, grad2.max())
g.zero_grad()

# --------------

r = g(q)
sm = r.sum()

start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
torch.cuda.synchronize()
start.record()

sm.backward()

end.record()
torch.cuda.synchronize()
print('fasttime', start.elapsed_time(end), 'ms')

grad1 = g.data.grad.clone()
print(grad1.shape, grad1.max())
g.zero_grad()


# --------------

print('err', torch.abs(grad1 - grad2).max().item())
