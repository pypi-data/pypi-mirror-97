"""
Image utilities.
================
Utility functions for image manipulation and visualization.
"""

from itertools import product
import matplotlib.pyplot as plt
import numpy as np


def matplotlib_imshow(img, one_channel=False, ax=None, **kwargs):
    if ax is None:
        ax = plt
    if one_channel:
        img = img.mean(dim=0)
    npimg = img.detach().cpu().numpy()
    if one_channel:
        ax.imshow(npimg, cmap="gray", **kwargs)
    else:
        ax.imshow(np.transpose(npimg, (1, 2, 0)), **kwargs)


def matplotlib_imshow_batch(batch, labels=None, one_channel=False, axes=None, normalize=False, range=(0., 1.),
                            title="", negative=False, **kwargs):
    npimgs = [img.detach().cpu().numpy() for img in batch]
    if labels is None:
        labels = [""] * batch.size(0)
    axes[0].set_title(title)
    for ax, img, label in zip(axes, npimgs, labels):
        if one_channel:
            if normalize:
                img = normalize_image(img, range, True, negative)
            ax.imshow(img, cmap='gray', **kwargs)
        else:
            img = np.transpose(img, (1, 2, 0))
            if normalize:
                img = normalize_image(img, range, False, negative)
            ax.imshow(img, **kwargs)

        ax.set_ylabel(label)
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.axis('off')



def normalize_image(img, range=(0., 1.), one_channel=False, negative=False):
    """
    Linearly normalizes an image to be in range.

    Supposes that img is in numpy image shape: (m, n, channels) or (m, n)
    """
    new_min, new_max = range
    old_min, old_max = img.min(), img.max()
    new = new_min + (img - old_min) * (new_max - new_min) / (old_max - old_min)
    if negative: 
        new = 1. - new
    return new


def group_patches(x_patch_size=8, y_patch_size=8, x_image_size=32, y_image_size=32, n_channels=3):
    groups = []
    for m in range(int(x_image_size / x_patch_size)):
        for p in range(int(y_image_size / y_patch_size)):
            groups.append([(c, m * x_patch_size + i, p * y_patch_size + j)
                           for c, i, j in product(range(n_channels),
                                                  range(x_patch_size),
                                                  range(y_patch_size))])
    return groups

