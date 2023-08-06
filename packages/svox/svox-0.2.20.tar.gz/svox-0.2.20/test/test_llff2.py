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

def load_poses_bounds(data_dir, factor=4):
    # Load poses and bds.
    with open(osp.join(data_dir, "poses_bounds.npy"), "rb") as fp:
        poses_arr : np.ndarray = np.load(fp)
    poses = poses_arr[:, :-2].reshape([-1, 3, 5])
    bds_min = poses_arr[:, -2:].min()
    focal = poses[0, -1, -1] / factor
    poses = poses[..., :-1]

    # Correct rotation matrix ordering
    default_transform = np.eye(4, dtype=np.float32)
    default_transform[:2, :2] = np.array([[0, -1], [1, 0]], dtype=np.float32)
    poses = poses @ default_transform

    # Rescale translation according to a default bd factor.
    poses[..., 3] *= 1.0 / (bds_min * 0.75)

    # Recenter poses (simplified version).
    mean_c2w = poses.mean(0)
    mean_c2w[..., 0] = np.cross(mean_c2w[..., 1], mean_c2w[..., 2])
    mean_c2w[..., 1] = np.cross(mean_c2w[..., 2], mean_c2w[..., 0])
    mean_c2w[:, :3] /= np.linalg.norm(mean_c2w[:, :3], axis=0, keepdims=True)
    poses[:, :3, 3:] -= mean_c2w[:3, 3:]
    poses = mean_c2w[:3, :3].T @ poses
    c2w = poses[:, :3, :4]

    return c2w.astype(np.float32), focal


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
    all_c2w, focal = load_poses_bounds(ROOT_DIR, FACTOR)
    images : np.ndarray = load_images(ROOT_DIR, FACTOR)
    height, width, _ = images[0].shape
    print(images.shape, all_c2w.shape)

    device = 'cuda'
    t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/nerf_llff_data/room.npz",
                          map_location=device)
    ndc = svox.NDCConfig(width=width, height=height, focal=focal)
    r = svox.VolumeRenderer(t, ndc=ndc)

    for i in range(images.shape[0]):
        c2w = torch.from_numpy(all_c2w[i]).cuda()
        c2w = torch.eye(4, device='cuda')
        rgb = r.render_persp(c2w, height=height, width=width, fx=focal, fast=True)
        rgb = rgb.reshape(height, width, 3).cpu().numpy()
        im_gt = images[i]
        print(rgb.shape, im_gt.shape, im_gt.max(), rgb.max())
        print(-10 * np.log10(((im_gt - rgb)**2).mean()))

        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(rgb)
        plt.subplot(1, 2, 2)
        plt.imshow(im_gt)
        plt.show()


if __name__ == '__main__':
    main()
