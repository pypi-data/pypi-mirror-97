# Copyright (c) 2020-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
# Copyright (c) 2020 Australian Plant Phenomics Facility
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from copy import deepcopy
from sys import stdin, stdout, stderr
from os.path import splitext
import os

from .base import PipelineStep
from ..timestream import FileContentFetcher


class UnsafeNuker(PipelineStep):
    """Attempts to delete TimestreamFile immediately."""

    def process_file(self, file):
        if not isinstance(file.fetcher, FileContentFetcher):
            print(f"WARNING: can't delete {file.filename} as it is bundled", file=stderr)
            return file
        os.unlink(file.fetcher.pathondisk)
        file.fetcher = None
        return file
