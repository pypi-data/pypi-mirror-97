import svox
import torch
import torch.cuda
from matplotlib import pyplot as plt  

device = 'cuda:0'

t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lego_diffscale.npz",
                      map_location=device)
#  t = svox.N3Tree(map_location=device)
r = svox.VolumeRenderer(t)
c2w = torch.tensor([
                [ -0.9999999403953552, 0.0, 0.0, 0.0 ],
                [ 0.0, -0.7341099977493286, 0.6790305972099304, 2.737260103225708 ],
                [ 0.0, 0.6790306568145752, 0.7341098785400391, 2.959291696548462 ],
                [ 0.0, 0.0, 0.0, 1.0 ],
            ], device=device)

with torch.no_grad():
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    im = None
    with t.accumulate_weights() as accum:
        start.record()
        for i in range(5):
            im = r.render_persp(c2w, height=800, width=800, fx=1111, cuda=True, fast=True)
        end.record()
    accum = accum()
    t[accum > 1, :1] = 100.0
    t[accum > 1, 1:16] = 0.0
    t[accum > 1, 16:3*16] = 0.0
    t[accum > 1, 3*16] = 100.0
    t.save('tmp.npz')

    torch.cuda.synchronize(device)
    dur = start.elapsed_time(end) / 5
    print('render time', dur, 'ms =', 1000 / dur, 'fps')
    print(im.shape)

    im = im.detach().clamp_(0.0, 1.0)
    plt.figure()
    plt.imshow(im.cpu())
    plt.show()
