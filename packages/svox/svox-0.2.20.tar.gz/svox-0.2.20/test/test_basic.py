import torch
import torch.nn.functional as F
import svox
from tqdm import tqdm

device='cuda:0'

g = svox.N3Tree(N=2, data_dim=3, map_location=device).to(device=device)

N = 12582912
#  N = 50331648
K = g.data_dim

torch.cuda.set_device(device)
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
torch.cuda.synchronize(device)

start.record()

print('prep')
print('begin refine')
for j in tqdm(range(500)):
    q = torch.rand((100, 3), device=device)
    g[q].refine()
    for i in range(20):
        q = torch.rand((1, 3), device=device)
        vals = 100 * torch.randn((1, K), device=device)
        g[q] = vals
print(g)

end.record()
torch.cuda.synchronize(device)
print('refine time', start.elapsed_time(end) / 10000, 'ms')

if True:
    torch.cuda.synchronize(device)
    print('begin fuzz')
    worst = 0.0
    for i in range(5000):
        q = torch.rand((1, 3), device=device)
        vals = 100 * torch.rand((1, K), device=device)
        g[q] = vals
        if i % 1000 == 999:
            for j in tqdm(range(100)):
                g[torch.rand((10, 3), device=device)].refine()
            print(g)
            print('current err', worst.item())
        r = g[q + 0.00000001 * (torch.rand_like(q) - 0.5)]
        err = torch.abs(r - vals).max()
        worst = max(torch.abs(r - vals).max(), worst)
    print('max err', worst.item())
    print('internal count', g.n_internal, 'max depth', g.max_depth)
    print('shape', g.data.shape)

if False:
    print('begin timing')
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    q = torch.rand((N, 3), device=device)
    torch.cuda.synchronize(device)
    start.record()

    for i in range(20):
        r = g(q, cuda=True)

    end.record()
    torch.cuda.synchronize(device)
    print('our time', start.elapsed_time(end) / 20, 'ms')

    X = torch.randn(1, 3, 64, 64, 64, device=device)
    G = torch.rand((1, 1, 1, N, 3), device=device) * 2 - 1

    # ----

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    torch.cuda.synchronize(device)

    start.record()
    for i in range(20):
        r = F.grid_sample(X, G, mode='nearest', align_corners=True)

    end.record()
    torch.cuda.synchronize(device)
    print('grid_sample time', start.elapsed_time(end) / 20, 'ms')
