from svox import csrc
import torch
import imageio
from matplotlib import pyplot as plt

im = imageio.imread("/home/sxyu/Pictures/angjoo.png")
H, W, C = im.shape

im = torch.from_numpy(im).reshape(-1, 3).float() / 255
colors, indices = csrc.quantize_median_cut(im, 8)

im = colors[indices.long()].reshape(H, W, 3)

plt.imshow(im)
plt.show()
