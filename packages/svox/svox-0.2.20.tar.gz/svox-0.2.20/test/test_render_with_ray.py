import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt

device = 'cuda:0'

t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lego_diffscale.npz",
#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/lego_v2_lo.npz",
#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/nerf_synthetic_v2/ship_v2.npz",
#  t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/mic_sg_sp.npz",
                      map_location=device)
#  t = svox.N3Tree(map_location=device)
r = svox.VolumeRenderer(t)
print(t)
c2w = torch.tensor([
                [ -0.9999999403953552, 0.0, 0.0, 0.0 ],
                [ 0.0, -0.7341099977493286, 0.6790305972099304, 2.737260103225708 ],
                [ 0.0, 0.6790306568145752, 0.7341098785400391, 2.959291696548462 ],
                [ 0.0, 0.0, 0.0, 1.0 ],
            ], device=device)

with torch.no_grad():
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    width = height = 800
    fx = fy = 1111
    origins = c2w[None, :3, 3].expand(height * width, -1).contiguous()
    yy, xx = torch.meshgrid(
        torch.arange(height, dtype=torch.float32, device=c2w.device),
        torch.arange(width, dtype=torch.float32, device=c2w.device),
    )
    xx = (xx - width * 0.5) / float(fx)
    yy = (yy - height * 0.5) / float(fy)
    zz = torch.ones_like(xx)
    dirs = torch.stack((xx, -yy, -zz), dim=-1)
    dirs /= torch.norm(dirs, dim=-1, keepdim=True)
    dirs = dirs.reshape(-1, 3)
    del xx, yy, zz
    dirs = torch.matmul(c2w[None, :3, :3], dirs[..., None])[..., 0]
    vdirs = dirs

    rays = svox.Rays(
        origins=origins,
        dirs=dirs,
        viewdirs=vdirs
    )

    im = None
    start.record()
    for i in range(5):
        im = r(rays, cuda=True, fast=True)
    end.record()

    torch.cuda.synchronize(device)
    dur = start.elapsed_time(end) / 5
    print('render time', dur, 'ms =', 1000 / dur, 'fps')
    print(im.shape)

    im = im.view(height, width, 3)

    im = im.detach().clamp_(0.0, 1.0)
    plt.figure()
    plt.imshow(im.cpu())
    plt.show()
