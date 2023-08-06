# Copyright (c) 2020-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
# Copyright (c) 2020 Australian Plant Phenomics Facility
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ..time import TSInstant
from ..utils import find_files
from ..timestream import *
from .base import *
from .imageio import TimestreamImage


import numpy as np
from pathlib import Path
from imageio import imread
from sys import stdin, stdout, stderr
from collections import defaultdict
import re


MASK_RE = re.compile(r"^(?P<name>\w+?)_?(?P<date>\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d)?$")


class Mask(object):
    """Mask: a smart loader of and  container for a boolean pixel mask."""

    def __init__(self, filename):
        self.filename = Path(filename)
        pix = imread(filename)
        if len(pix.shape) == 2:
            # already grey
            mask = pix != 0
        if len(pix.shape) == 3:
            # colour, needs flattening
            if pix.shape[2] == 4:
                pix =  pix[:,:,:2]
            mask = pix.mean(axis=2) <= 1
        self.mask = mask.astype(bool)
        self.mask_sum = mask.sum()
    
    def apply(self, other):
        """Apply this mask to some image, returning a copy of `other` with non-hot regions blacked out"""
        res = other.copy()
        res[self.mask != True] = 0
        return res
    
    def __repr__(self):
        x, y = self.mask.shape
        return f"Mask of {x}x{y} pixels (sum: {self.mask_sum})"


class ROIMaskManager(object):
    """ROIMaskManager: A collection of ROI masks, and logic for selecting the mask(s) applicable to some image"""

    def __init__(self, mask_imagedir):
        self.maskdir = Path(mask_imagedir)
        self._find_masks()
    
    def _find_masks(self):
        """Finds mask files on disk"""
        masks = defaultdict(dict)
        for p in map(Path, find_files(self.maskdir)):
            if p.suffix.lower() not in {".jpg", ".png"}:
                print(f"WARNING: non-image file in mask directory ignored {str(p)}", file=stderr)
            m = MASK_RE.match(p.stem)
            if m is None:
                print(f"WARNING: skipping badly-named mask image '{str(p)}'", file=stderr)
            m = m.groupdict()

            mask_name = m["name"]
            if m["date"] is None:
                m["date"] = "1700_01_01_00_00_00"
            instant = TSInstant(m["date"])

            masks[mask_name][instant] = Mask(p)

        self.masks = masks
    
    def find_applicable_masks(self, image):
        """Selects masks from this catalogue which apply to `image`"""
        m = {}
        for mask in self.masks:
            whichtime = None
            for maskdt in sorted(self.masks[mask].keys()):
                if maskdt <= image.instant:
                    whichtime = maskdt
                if whichtime is not None:
                    m[mask] = self.masks[mask][whichtime]
        return m
    
    def generate_masked_images(self, image):
        """For each mask in this catalogue applicable to `image`, return a pixel-masked TimestreamImage"""
        appl_masks = self.find_applicable_masks(image)
        for maskname, mask in appl_masks.items():
            this = image.copy()
            this.instant.index = maskname
            this.mask =  mask.mask
            this.pixels =  mask.apply(this.pixels)
            this.report["ROIMaskName"] = maskname
            this.report["ROIMaskSum"] = mask.mask_sum
            yield this
    
    def __repr__(self):
        return f"ROIMaskManager with {len(self)} masks"
    
    def __len__(self):
        return len(self.masks)


class ROIPipelineStep(PipelineStep):
    """Step to extract per-ROI images and run subsequent pipeline on each ROI independently.

    Notes to users:

        - ROI mask images should be the exact dimensions of source images
        - ROI masks should have black pixels for regions that SHOULD be
          selected. Yes, this is the opposite of what logic might suggest, but
          it's what the US phenocam network does.
        - Each output image takes the basename of the input image, but adds the
          ROI name as a sub-second index (after the time field).
    """

    def __init__(self, rois, other_pipeline):
        if not isinstance(rois, ROIMaskManager):
            rois = ROIMaskManager(rois)
        self.rois = rois
        self.pipe = other_pipeline

    def finish(self):
        self.pipe.finish()
        self.report = self.pipe.report

    def process_file(self, file):
        for resimg in self.rois.generate_masked_images(file):
            self.pipe.process_file(resimg)
        return file
