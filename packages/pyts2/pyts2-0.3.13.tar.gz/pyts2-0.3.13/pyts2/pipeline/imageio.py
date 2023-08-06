# Copyright (c) 2018-2021 Kevin Murray <foss@kdmurray.id.au>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import numpy as np
import os
os.environ["OMP_NUM_THREADS"] = "1"  # force single-threaded demosaicing in rawpy
import rawpy
import cv2
import imageio
import skimage as ski
from skimage.color import rgb2lab
from PIL import Image

from ..time import *
from ..utils import *
from ..timestream import *
from .base import PipelineStep, AbortPipelineForThisImage

import datetime as dt
import os.path as op
from sys import stderr, stdout, stdin
import re
import io
import sys


class DecodeImageFileStep(PipelineStep):
    """Pipeline step to decode image pixels from binary file content, optionally
    converting raw image formats to a standard numpy array.
    """

    default_options = {
        "jpg": {},
        "tif": {},
        "png": {},
        "cr2": {
            "use_camera_wb": True,
            "median_filter_passes": 0,  # no median filtering after demosaicing
            "output_bps": 16,
            "auto_bright_thr": 0.001,  # Use auto brightness, but only allow clipping 0.1%
        },
    }

    def __init__(self, decode_options=None, process_raws=True, raw_use_embedded_jpeg=False):
        """
        :param decode_options: Options for processing raw images
        :type decode_options: list, optional
        :param process_raws: Process raw image
        :type process_raws: bool
        :param raw_use_embedded_jpeg: Use the jpg embedded in the raw image, if available
        :type raw_use_embedded_jpeg: bool
        """
        self.raw_use_embedded_jpeg = raw_use_embedded_jpeg
        self.decode_options = self.default_options
        if decode_options:
            self.decode_options.update(self.decode_options)
        self.process_raws = process_raws

    def process_file(self, file):
        base, ext = op.splitext(file.filename)
        format = ext.lower().strip(".")
        try:
            if format in ("cr2", "nef", "rw2"):
                with rawpy.imread(io.BytesIO(file.content)) as img:
                    if self.process_raws:
                        pixels = img.postprocess(**self.decode_options[format].copy())
                    elif self.raw_use_embedded_jpeg:
                        try:
                            thumb = raw.extract_thumb()
                        except (rawpy.LibRawNoThumbnailError, rawpy.LibRawUnsupportedThumbnailError) as exc:
                            pixels = img.postprocess(**self.decode_options[format].copy())
                        else:
                            pixels = imageio.imread(thumb.data)
                    else:
                        pixels = img.raw_image.copy()
            else:
                pixels = imageio.imread(file.content)
        except Exception as exc:
            raise AbortPipelineForThisImage(f"Error on image read: {exc.__class__.__name__}: {str(exc)}")
        return TimestreamImage.from_timestreamfile(file, pixels=pixels)


class EncodeImageFileStep(PipelineStep):
    """Pipeline step to encode pixels to a file('s bytes)."""
    default_options = {
        "jpg": {
            "format": "JPEG-PIL",  # engine
            "quality": 95,
            "progressive": True,
            "optimize": True,
            "subsampling": "4:4:4",
        },
        "tif": {
            # These are arugments to PIL's image.save. See note below in process_file
            "format": "TIFF",
            "compression": "tiff_lzw"
        },
        "png": {
            "format": "PNG",  # engine
            "optimize": True,
        },
    }

    def __init__(self, format="tiff", encode_options=None):
        """
        :param format: Image type to encode as (``tiff/jpg/png``)
        :type format: str
        :param encode_options: Encoding options passed to PIL
        :type encode_options: list, optional
        """
        # Normalise format
        format = format.lower()
        if format == "jpeg":
            format = "jpg"
        if format == "tiff":
            format = "tif"

        if format not in self.default_options:
            raise ValueError("Unsupported image format '{}'".format(format))
        self.format = format

        self.options = self.default_options[self.format].copy()
        if encode_options:
            self.options.update(encode_options)

    def process_file(self, file):
        if not isinstance(file, TimestreamImage):
            raise TypeError("EncodeImageFile operates on TimestreamImage (not TimestreamFile)")

        base, ext = op.splitext(file.filename)
        filename = f"{base}.{self.format}"

        # TODO: encode exif data for tiff & jpeg
        if self.format == "tif":
            # So tiffs are a bit broken in imageio at the moment. Therefore we need some
            # manual hackery with PIL
            with io.BytesIO() as buf:
                file.pil.save(buf, **self.options)
                content = buf.getvalue()
        elif self.format == "png" or self.format == "jpg":
            content = imageio.imwrite('<bytes>', file.rgb_8, **self.options)
        # reinstatiate and demote to a TimestreamFile
        return TimestreamFile(content=content, filename=filename,
                              instant=file.instant, report=file.report,
                              format=self.format)


class TimestreamImage(TimestreamFile):
    """Image class for all timestreams"""

    def __init__(self, instant=None, filename=None, fetcher=None, content=None,
                 report=None, pixels=None, exifdata=None):
        """
        :param instant: Datetime point that this file represents
        :type instant: TSInstant object or derived from file path
        :param filename: Name of file, can be retrieved from fetcher
        :type filename: str
        :param fetcher: File fetcher object to retrieve file content from disk or within archive formats
        :type fetcher: :class:`.Fetcher`, optional
        :param content: File content (usually if creating timestream file in pipelines)
        :type content: File content, optional
        :param report: Variable to store reports from Timestream pipeline components
        :type report: dict
        :param pixels: Pixels as an array format
        :type pixels: np.array or similar, optional
        :param exifdata: Unimplemented
        :type exifdata: None
        """
        super().__init__(instant, filename, fetcher, content, report)
        self._pixels = None
        if pixels is not None:
            self._pixels = ski.img_as_float(pixels)
        self.exifdata = exifdata  # where does this get used?

    def save(self, outpath):
        """Writes file to ``outpath``, in whatever format the extension of ``outpath`` suggests.

        :param outpath: Path of output file
        :type outpath: str
        """
        imageio.imwrite(outpath, self.pixels)

    @property
    def rgb_8(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return ski.img_as_ubyte(self.pixels)

    @property
    def rgb_16(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return ski.img_as_uint(self.pixels)

    @property
    def bgr_8(self):
        return self.rgb_8[:, :, ::-1]  # RGB->BGR

    @property
    def Lab(self):
        return rgb2lab(self.pixels)

    @property
    def pixels(self):
        return self._pixels

    @property
    def content(self):
        return super().content

    @content.setter
    def content(self, value):
        self._pixels = None  # invalidate pixels
        self._content = value

    @pixels.setter
    def pixels(self, value):
        self._pixels = ski.img_as_float(value)
        self._content = None  # invalidate content, as we've updated the pixels

    @property
    def pil(self):
        return Image.fromarray(self.rgb_8)

    @staticmethod
    def from_path(path):
        file = TimestreamFile.from_path(path)
        return DecodeImageFileStep().process_file(file)

    @classmethod
    def from_timestreamfile(cls, file, **kwargs):
        """Convenience creator for TSFile -> TSImage conversion"""
        params = {
            "instant": file.instant,
            "filename": file.filename,
            "fetcher": file.fetcher,
            "report": file.report,
            "content": file.content,
        }
        params.update(kwargs)
        return cls(**params)
