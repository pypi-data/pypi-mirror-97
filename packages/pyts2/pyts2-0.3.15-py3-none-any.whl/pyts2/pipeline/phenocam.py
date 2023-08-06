# Copyright (c) 2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ..time import *
from ..utils import *
from ..timestream import *
from .base import *
from .imageio import *

import numpy as np

class PhenocamRGBMetricStep(PipelineStep):
    """
    Reports RGB colour metrics (percentiles, means, sd, chromatic coordinates,
    colour excesses) used by the Phenocam project to monitor ecosystems.
    """
    def process_file(self, file):
        assert hasattr(file, "pixels")
        # these metrics are defined over a typical 8-bit RGB image
        pix = file.rgb_8
        
        # First, we get either the pixels correpsonding to the masked area, if
        # `file` has an applicable mask. Otherwise, we just reshape all pixels
        # to be the same shape as if a mask selecting all pixels had been
        # applied.
        if hasattr(file, "mask"):
            pix = pix[file.mask]  # should give a N_pixels_selected x N_channels array
        else:
            # npixels x nchannels array
            pix = pix.reshape(-1, pix.shape[-1])
        assert len(pix.shape) == 2

        # Vectors corresponding to all red, green, blue channel values (called
        # digital number/DN in literature) for each of the HxW pixels
        R = pix[:,0].flatten()
        G = pix[:,1].flatten()
        B = pix[:,2].flatten()

        # Here we set the percentiles and mean/sd for each channel in a loop
        orig = {"R": R, "G": G, "B": B}
        metrics = {}
        for chan in "RGB":
            for pct in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
                metrics[f"{chan}_{pct:02d}pct"] = np.percentile(orig[chan], pct)
            metrics[f"{chan}_mean"] = np.mean(orig[chan])
            metrics[f"{chan}_sd"] = np.std(orig[chan])

        # Pearson's r for each channel pair. N.B: np.corrcoef gives a VCV-like
        # matrix of R values, like:
        # [[1, r],
        #  [r, 1]]
        # so we have to grab the off-diagonal value with the [0, 1] subset.
        metrics["RG_cor"] = np.corrcoef(R, G)[0, 1]
        metrics["RB_cor"] = np.corrcoef(R, B)[0, 1]
        metrics["GB_cor"] = np.corrcoef(G, B)[0, 1]

        # the last set of metrics are calculated as means, so we calculate the
        # metric of the mean, rather than the mean of the metric. So we save 
        # r, g, b as the means of each channel.
        r = R.mean()
        g = G.mean()
        b = B.mean()
        metrics["ExR"] = (2 * r) - (g + b)
        metrics["ExG"] = (2 * g) - (r + b)
        metrics["ExB"] = (2 * b) - (r + g)
        metrics["Rcc"] = r / (r + g + b)
        metrics["Gcc"] = g / (r + g + b)
        metrics["Bcc"] = b / (r + g + b)
        file.report.update(metrics)
        return file
