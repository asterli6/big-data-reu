import numpy as np
import torch

class MinMaxEmissiveScaleReflectance(object):
    """
    Performs scaling of MODIS TOA data
    - Scales reflectance percentages to reflectance units (% -> (0,1))
    - Performs per-channel minmax scaling for emissive bands (k -> (0,1))
    """

    def __init__(self):

        self.reflectance_indices = [0, 1, 2, 3, 4, 6]
        self.emissive_indices = [5, 7, 8, 9, 10, 11, 12, 13]

        self.emissive_mins = torch.tensor(
            [117.04327, 152.00592, 157.96591, 176.15349,
             210.60493, 210.52264, 218.10147, 225.9894],
            dtype=torch.float32)

        self.emissive_maxs = torch.tensor(
            [221.07022, 224.44113, 242.3326, 307.42004,
             290.8879, 343.72617, 345.72894, 323.5239],
            dtype=torch.float32)

    def __call__(self, img):
        # img: tensor (C,H,W)

        # Reflectance % to reflectance units
        img[self.reflectance_indices,:,:] *= 0.01

        # Brightness temp scaled to (0,1) range
        mins = self.emissive_mins[:, None, None]
        maxs = self.emissive_maxs[:, None, None]

        img[self.emissive_indices, :, :] = (img[self.emissive_indices, :, :] - mins) / (maxs - mins)
        return img

