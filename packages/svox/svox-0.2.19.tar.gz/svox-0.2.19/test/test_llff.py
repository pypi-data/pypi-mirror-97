import numpy as np
import os.path as osp
import os
import svox
import torch
import imageio
from matplotlib import pyplot as plt

ROOT_DIR = '/home/sxyu/data/nerf/nerf_llff_data/room'
FACTOR = 4
LLFFHOLD = 8

def _normalize(x):
    """Normalization helper function."""
    return x / np.linalg.norm(x)

def _viewmatrix(z, up, pos):
    """Construct lookat view matrix."""
    vec2 = _normalize(z)
    vec1_avg = up
    vec0 = _normalize(np.cross(vec1_avg, vec2))
    vec1 = _normalize(np.cross(vec2, vec0))
    m = np.stack([vec0, vec1, vec2, pos], 1)
    return m

def _poses_avg(poses):
    """Average poses according to the original NeRF code."""
    hwf = poses[0, :3, -1:]
    center = poses[:, :3, 3].mean(0)
    vec2 = _normalize(poses[:, :3, 2].sum(0))
    up = poses[:, :3, 1].sum(0)
    c2w = np.concatenate([_viewmatrix(vec2, up, center), hwf], 1)
    return c2w


def _recenter_poses(poses):
    """Recenter poses according to the original NeRF code."""
    poses_ = poses.copy()
    bottom = np.reshape([0, 0, 0, 1.0], [1, 4])
    c2w : np.ndarray = _poses_avg(poses)
    c2w = np.concatenate([c2w[:3, :4], bottom], -2)
    bottom = np.tile(np.reshape(bottom, [1, 1, 4]), [poses.shape[0], 1, 1])
    poses = np.concatenate([poses[:, :3, :4], bottom], -2)
    poses = np.linalg.inv(c2w) @ poses
    poses_[:, :3, :4] = poses[:, :3, :4]
    poses = poses_
    return poses


def load_poses_bounds(data_dir, factor=4):
    # Load poses and bds.
    with open(osp.join(data_dir, "poses_bounds.npy"), "rb") as fp:
        poses_arr : np.ndarray = np.load(fp)
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1, 2, 0])
    bds = poses_arr[:, -2:].transpose([1, 0])

    print('poses', poses.shape)

    # Update poses according to downsampling.
    poses[:2, 4, :] /= factor
    poses[2, 4, :] /= factor

    # Correct rotation matrix ordering and move variable dim to axis 0.
    poses = np.concatenate(
        [poses[:, 1:2, :], -poses[:, 0:1, :], poses[:, 2:, :]], 1
    )
    print('poses', poses.shape)
    poses = np.moveaxis(poses, -1, 0).astype(np.float32)
    bds = np.moveaxis(bds, -1, 0).astype(np.float32)
    print('poses', poses.shape)

    # Rescale according to a default bd factor.
    scale = 1.0 / (bds.min() * 0.75)
    poses[:, :3, 3] *= scale
    bds *= scale

    # Recenter poses.
    poses = _recenter_poses(poses)
    c2w = poses[:, :3, :4]
    focal = poses[0, -1, -1]

    return c2w, focal, bds


def load_images(data_dir, factor=4):
    imgdir_suffix = ""
    if factor > 1:
        imgdir_suffix = "_{}".format(factor)
        factor = factor
    imgdir = osp.join(data_dir, "images" + imgdir_suffix)
    if not osp.isdir(imgdir):
        raise ValueError("Image folder {} doesn't exist.".format(imgdir))
    imgfiles = [
        osp.join(imgdir, f)
        for f in sorted(os.listdir(imgdir))
        if f.endswith("JPG") or f.endswith("jpg") or f.endswith("png")
    ]
    images = []
    for imgfile in imgfiles:
        image = imageio.imread(imgfile).astype(np.float32) / 255.0
        images.append(image)
    return np.stack(images)

@torch.no_grad()
def main():
    all_c2w, focal, bds = load_poses_bounds(ROOT_DIR, FACTOR)
    images : np.ndarray = load_images(ROOT_DIR, FACTOR)
    height, width, _ = images[0].shape
    print(images.shape, all_c2w.shape)

    device = 'cuda'
    t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/llff_room.npz",
                          map_location=device)
    ndc = svox.NDCConfig(width=width, height=height, focal=focal)
    r = svox.VolumeRenderer(t, ndc=ndc)

    for i in range(images.shape[0]):
        c2w = torch.from_numpy(all_c2w[i]).cuda()
        rgb = r.render_persp(c2w, height=height, width=width, fx=focal, fast=True)
        rgb = rgb.reshape(height, width, 3).cpu().numpy()
        #  im_gt = images[i]
        #  print(rgb.shape, im_gt.shape, im_gt.max(), rgb.max())
        #  print(-10 * np.log10(((im_gt - rgb)**2).mean()))

        plt.figure()
        #  plt.subplot(1, 2, 1)
        plt.imshow(rgb)
        #  plt.subplot(1, 2, 2)
        #  plt.imshow(im_gt)
        plt.show()

if __name__ == '__main__':
    main()
