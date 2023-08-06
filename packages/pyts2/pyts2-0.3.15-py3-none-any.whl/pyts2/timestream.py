# Copyright (c) 2018 Kevin Murray <kdmfoss@gmail.com>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tqdm import tqdm

import copy
import datetime as dt
import hashlib
import io
import os
import os.path as op
import json
from pathlib import Path
from queue import Queue
import re
from sys import stderr, stdout, stdin
import tarfile
from threading import Thread
import traceback
import warnings
import zipfile
import zlib

from pyts2.time import *
from pyts2.utils import *
from pyts2.filelock import FileLock

def get_instant_or_fn(path):
    try:
        return str(TSInstant.from_path(path))
    except ValueError:
        return path


def path_is_timestream_file(path, extensions=None):
    """Test if path given contains a valid timestream format, and optionally
    checks that it has an expected file extension.

    :param path: File path, with or without directory
    :type path: str
    :param extensions: Optionally, one or more extensions to accept
    :type extensions: str
    :return: True if path is timestream and extension compatible, otherwise False
    :rtype: bool

    >>> path_is_timestream_file("test_2018_12_31_23_59_59_00.jpg")
    True
    >>> path_is_timestream_file("test_2018_12_31_23_59_59_00_1.jpg")
    True
    >>> path_is_timestream_file("2018_12_31_23_59_59_00.jpg")
    True
    >>> path_is_timestream_file("test_2018_12_31_23_59_59_00.jpg", extensions="jpg")
    True
    >>> path_is_timestream_file("test_2018_12_31_23_59_59_00.jpg", extensions="tif")
    False
    >>> path_is_timestream_file("not-a-timestream.jpg")
    False
    """
    if extensions is None:
        extensions = []
    if isinstance(extensions, str):
        extensions = [extensions, ]
    extensions = set(extensions)
    if "tif" in extensions:
        extensions.add("tiff")
    if "tiff" in extensions:
        extensions.add("tif")
    if "jpg" in extensions:
        extensions.add("jpeg")
    if "jpeg" in extensions:
        extensions.add("jpg")
    try:
        m = TS_DATETIME_RE.search(path)
        if m is None:
            return False
        if extensions:
            return any([path.lower().endswith(f".{ext}") for ext in extensions])
        return True
    except ValueError:
        return False


class Fetcher(object):
    """ Gets files from archive bundles.
    """
    @classmethod
    def from_json(self, obj):
        """ Takes an object path and returns format-decoded file content.

        :param obj: File object to look up
        :type obj: JSON object/dict
        :return: Fetched file
        :rtype: File content
        """
        if obj["type"] == "zip":
            return ZipContentFetcher(obj["archivepath"], obj["pathinzip"])
        elif obj["type"] == "tar":
            return TarContentFetcher(obj["archivepath"], obj["pathintar"])

    @property
    def instant(self):
        """ Gets datetime from file path.

        :return: Datetime
        :rtype: :class:`.TSInstant`
        """
        return TSInstant.from_path(self.filename)


class ZipContentFetcher(Fetcher):
    """ Retrieves files from zip archives.
    """
    _fetchtype = 'zip'

    def __init__(self, archivepath, pathinzip):
        """
        :param archivepath: Path to zip file
        :type archivepath: str
        :param pathinzip: Path to file to retrieve, within zip
        :type pathinzip: str
        """
        self.archivepath = archivepath
        self.pathinzip = pathinzip

    def get(self):
        """
        :return: File retrieved from zip archive.
        :rtype: File content
        """
        with zipfile.ZipFile(str(self.archivepath)) as zfh:
            return zfh.read(self.pathinzip)

    @property
    def filename(self):
        return op.basename(self.pathinzip)

    def dict(self):
        """
        :return: Summary of fetch parameters
        :rtype: dict
        """
        return {"type": "zip",
                "archivepath": self.archivepath,
                "pathinzip": self.pathinzip}


class TarContentFetcher(Fetcher):
    """ Retrieves files from tar archives.
    """
    _fetchtype = 'tar'

    def __init__(self, archivepath, pathintar):
        """
        :param archivepath: Path to tar file
        :type archivepath: str
        :param pathinzip: Path to file to retrieve, within tar file
        :type pathinzip: str
        """
        self.archivepath = archivepath
        self.pathintar = pathintar

    def get(self):
        """
        :return: File retrieved from tar archive.
        :rtype: File content
        """
        with tarfile.TarFile(self.archivepath) as tfh:
            return tfh.extractfile(self.pathintar).read()

    @property
    def filename(self):
        return op.basename(self.pathintar)

    def dict(self):
        """
        :return: Summary of fetch parameters
        :rtype: dict
        """
        return {"type": "tar",
                "archivepath": self.archivepath,
                "pathintar": self.pathintar}


class FileContentFetcher(Fetcher):
    """ Retrieves files from disk, not in an archive.
    """

    def __init__(self, path):
        """
        :param path: Path to file to retrieve
        :type path: str
        """
        self.pathondisk = Path(path)

    def get(self):
        """
        :return: File retrieved from disk.
        :rtype: File content
        """
        with open(self.pathondisk, "rb") as fh:
            return fh.read()

    @property
    def filename(self):
        return op.basename(self.pathondisk)

    def dict(self):
        """
        :return: Summary of fetch parameters
        :rtype: dict
        """
        return {"type": "file",
                "path": self.pathondisk}


class TimestreamFile(object):
    '''A container class for files in timestreams'''

    def __init__(self, instant=None, filename=None, fetcher=None, content=None, report=None, format=None):
        """
        :param instant: Datetime point that this file represents
        :param filename: Name of file, can be retrieved from fetcher
        :param fetcher: File fetcher object to retrieve file content from disk or within archive formats
        :param content: File content (usually if creating timestream file in pipelines)
        :param report: Variable to store reports from Timestream pipeline components
        :param format: File format, often the file extension (e.g. ``jpg``)
        :type instant: TSInstant object or derived from file path
        :type filename: str
        :type fetcher: :class:`.Fetcher`, optional
        :type content: File content, optional
        :type report: dict
        :type format: str, optional
        """
        self.instant = instant
        self.filename = filename
        self.fetcher = fetcher
        if filename is None and fetcher is not None:
            self.filename = fetcher.filename
        self._content = content
        # a report from various pipeline components on this file
        if report is None:
            report = dict()
        self.report = report
        if self.instant is None and self.filename is not None:
            self.instant = TSInstant.from_path(self.filename)
        if self.instant is None:
            raise ValueError("TimestreamFile must have an instant")
        if self.filename is None:
            raise ValueError("TimestreamFile must have a filename")
        if self.__class__ is TimestreamFile and self._content is None and self.fetcher is None:
            raise ValueError("TimestreamFile must have content (directly or via a fetcher)")
        if format is None:
            format = op.splitext(self.filename)[1]
        self.format = format.lower().lstrip(".")

    @property
    def content(self):
        if self._content is None and self.fetcher is not None:
            self._content = self.fetcher.get()
        if self._content is None:
            self._content = b''
        return self._content

    def clear_content(self):
        """ Deletes all file content in object.
        """
        del self._content
        self._content = None
        if hasattr(self, '_pixels'):
            del self._pixels
            self._pixels = None

    # TODO: work out where this should go. be careful, as setting here should sync to
    # disc perhaps?
    # @content.setter
    # def _set_content(self, content):
    #    self._content = content

    @classmethod
    def from_path(cls, path, instant=None):
        """ Create timestream file from file path.

        :param path: Path to file
        :type path: str
        :param instant: Timepoint associated with object. Attempts to use datetime in path if not provided.
        :type instant: :class:`time.TSInstant`, optional
        :return: Timestream file
        :rtype: :class:`.TimestreamFile`
        """
        if instant is None:
            instant = TSInstant.from_path(path)
        return cls(fetcher=FileContentFetcher(path),
                   filename=op.basename(path),
                   instant=instant)

    @classmethod
    def from_bytes(cls, filebytes, filename, instant=None):
        """ Create timestream file programmatically.

        :param filebytes: Bytes to encode
        :type filebytes: bytes
        :param filename: Name of file
        :type filename: str
        :param instant: Timepoint associated with object. Attempts to use datetime in path if not provided.
        :type instant: :class:`time.TSInstant`, optional
        :return: Timestream file
        :rtype: :class:`.TimestreamFile`
        """
        if not isinstance(filebytes, bytes):
            raise ValueError("from_bytes must be given file contents as bytes")
        if instant is None:
            instant = TSInstant.from_path(filename)
        return cls(content=filebytes, filename=filename, instant=instant)

    def isodate(self):
        """convenience helper to get iso8601 string"""
        return self.instant.isodate("%Y-%m-%dT%H:%M:%S")

    def __len__(self):
        return len(self.content)

    def checksum(self, algorithm="md5"):
        """ Checksum content of this object by the given algorithm.

        :param algorithm: Algorithm name supported by :class:`hashlib`
        :type algorithm: str, optional
        :return: Checksum of file contents
        :rtype: string object of double length, containing only hexadecimal digits
        """
        hasher = hashlib.new(algorithm)
        hasher.update(self.content)
        return hasher.hexdigest()

    def __repr__(self):
        return self.filename

    @property
    def md5sum(self):
        return self.checksum('md5')

    @property
    def shasum(self):
        return self.checksum('sha512')

    def copy(self):
        return copy.deepcopy(self)


class TimeStream(object):
    """ Represents a set of files organised in Timestream format.
    """
    bundle_levels = ("root", "year", "month", "day", "hour", "none")

    def __init__(self, path=None, format=None,
                 bundle_level="none", name=None, timefilter=None,
                 add_subsecond_field=False, flat_output=False,
                 write_index=False):
        """
        :param path: Base directory of a timestream
        :type path: str
        :param format: Format of files in timestream, usually the same as the file extension (e.g. ``.jpg``)
        :type format: str
        :param bundle_level: Smallest time unit to bundle files at.
        :type bundle_level: str
        :param name: Name of timestream
        :type name: str
        :param timefilter: Timefilter object for defining datetime range to iterate over
        :type timefilter: :class:`time.Timefilter`, optional
        :param add_subsecond_field: Enable for timestreams with sub-second records, using an additional ``_[00-99]`` at the end of filenames
        :type add_subsecond_field: bool, optional
        :param flat_output: Store timestream in a flat file structure, instead of Timestream directory structure
        :type flat_output: bool, optional
        :param write_index: Save file paths in timestream to an index.json file
        :type write_index: bool, optional
        """
        self._files = {}
        self._instants = {}
        self.name = name
        self.path = None
        if format is not None:
            format = format.lstrip(".").lower()
            if format == "tiff":
                format = "tif"
            if format == "jpeg":
                format = "jpg"
        self.format = format
        self.sorted = True
        self.write_index = write_index
        self.add_subsecond_field = add_subsecond_field
        self.flat_output = flat_output
        if timefilter is not None and not isinstance(timefilter, TimeFilter):
            raise ValueError("TimeFilter is not valid")
        self.timefilter = timefilter
        if bundle_level not in self.bundle_levels:
            raise ValueError("invalid bundle level %s",  bundle_level)
        self.bundle = bundle_level
        self._index_file = None
        if path is not None:
            self.open(path, format=format)
            if bundle_level == "root" or op.isfile(self.path):
                self._index_file = self.path + ".index.json"
            else:
                self._index_file = op.join(self.path, "index.json")

    def open(self, path, format=None):
        """ Opens a stored timestream.

        :param path: Path to timestream file/directory
        :type path: str
        :param format: Timestream format, if not unarchived or in a tar/zip archive
        :type format: str, optional
        """
        if self.name is None:
            self.name = op.basename(path)
            for ext in [".tar", ".zip", f".{format}"]:
                if self.name.lower().endswith(ext):
                    self.name = self.name[:-len(ext)]
        self.path = path

    def index(self, progress=True):
        """ Update timestream index if empty. Useful before searching a
        timestream for specific timepoints. Also updates index file if one is
        set/exists.

        :param progress: Show progress of indexing with :class:`tqdm`
        :type progress: bool, optional
        """
        if len(self._instants) == 0 or len(self._files) == 0:
            with FileLock(self._index_file, timeout=3600):
                pass
            try:
                if op.exists(self._index_file):  # TODO FIXME make this check if the index is stale
                    print("read index", self._index_file, file=stderr)
                    with open(self._index_file, "r") as fh:
                        self._files = {}
                        self._instants = {}
                        for line in tqdm(fh):
                            fetcher = Fetcher.from_json(json.loads(line))
                            self._files[fetcher.filename] = fetcher
                            self._instants[fetcher.instant] = fetcher
                        if len(self._instants) > 0 and len(self._files) > 0:
                            return
            except Exception as exc:
                print("Failed to load index file:", str(exc), file=stderr)
                if stderr.isatty():
                    traceback.print_exc(file=stderr)
            with FileLock(self._index_file):
                try:
                    itr = self.iter(tar_contents=False)
                    if progress:
                        itr = tqdm(itr)
                    if self.write_index:
                        with open(self._index_file, "w") as fh:
                            for f in itr:
                                self._instants[f.instant] = f.fetcher
                                print(json.dumps(f.fetcher.dict(), cls=PathAwareJsonEncoder), file=fh)
                    else:
                        for f in itr:
                            self._instants[f.instant] = f.fetcher
                except Exception as exc:
                    print("Failed to create timestream index file:", str(exc), file=stderr)
                    if stderr.isatty():
                        traceback.print_exc(file=stderr)
                    if op.exists(self._index_file):
                        os.unlink(self._index_file)

    @property
    def instants(self):
        self.index(progress=False)
        return self._instants.keys()

    def getinstant(self, value):
        """ Retrieves files from timestream at a specific time point.

        :param value: Time point to retrieve
        :type value: :class:`time.TSInstant`
        :return: File if present
        :rtype: :class:`.TimestreamFile`
        """
        if isinstance(value, TimestreamFile):
            value = value.instant
        assert(isinstance(value, TSInstant))
        self.index(progress=False)
        fetcher = self._instants[value]
        return TimestreamFile(filename=fetcher.filename, fetcher=fetcher)

    def __getitem__(self, filename):
        self.index(progress=False)
        return TimestreamFile(filename=filename, fetcher=self._files[filename])

    def _scan_dir(self, basedir):
        for root, dirs, files in os.walk(basedir):
            # ensure sorted iteration
            dirs.sort()
            files.sort(key=lambda f: get_instant_or_fn(f))
            for file in files:
                path = op.join(root, file)
                if not op.exists(path):
                    continue
                if file.startswith('.'):
                    continue
                if not path_is_timestream_file(path, extensions=self.format):
                    continue
                fetcher = FileContentFetcher(path)
                self._files[fetcher.filename] = fetcher
                yield TimestreamFile(fetcher=fetcher)

    def from_inotify(self, basedir):
        """ Watch a directory for files using ``inotify`` and yield new files as they are added to it.
        Rescans every 10 minutes.

        :param basedir: Directory to watch.
        :type basedir: str
        """
        import inotify.adapters

        while True:
            # this dual loop means we should time out and re-scan the complete dir every hour or so
            yield from self._scan_dir(basedir)

            inot = inotify.adapters.InotifyTree(basedir)
            for _ in range(600): # rescan every 10m
                for ev in inot.event_gen(timeout_s=1, yield_nones=False):
                    (_, type_names, path, filename) = ev
                    if 'IN_ISDIR' in type_names or not 'IN_CLOSE_WRITE' in type_names and not 'IN_MOVED_TO' in type_names:
                        continue
                    path = op.join(path, filename)
                    if filename.startswith('.') or not op.exists(path) or not path_is_timestream_file(path, extensions=self.format):
                        continue
                    fetcher = FileContentFetcher(path)
                    self._files[fetcher.filename] = fetcher
                    yield TimestreamFile(fetcher=fetcher)
            # clean up inotify watcher
            del inot



    def from_fofn(self, pathorfile):
        """ Yields files from a list of file names, most commonly from an index file.

        :param pathorfile: Path to an index file, or open file of file names
        :type pathorfile: str or :class:`io.IOBase`
        :return: Iteratively returns files from file names
        :rtype: :class:`.TimestreamFile`
        """
        fp = pathorfile
        if not isinstance(pathorfile, io.IOBase):
            fp = open(pathorfile)
        for path in fp:
            path = path.strip()
            if not path_is_timestream_file(path, extensions=self.format):
                continue
            fetcher = FileContentFetcher(path)
            self._files[fetcher.filename] = fetcher
            yield TimestreamFile(fetcher=fetcher)

    def iter(self, tar_contents=True):
        """ Yields files in timestream, sorted by time.

        :param tar_contents: Load tar contents into TimestreamFile immediately, rather than through TarContentFetcher
        :type tar_contents: bool, optional
        :return: Timestream files, iteratively
        :rtype: :class:`.TimestreamFile`
        """
        def walk_archive(path):
            if zipfile.is_zipfile(str(path)):
                with zipfile.ZipFile(str(path)) as zip:
                    # ensure sorted iteration
                    entries = zip.infolist()
                    entries.sort(key=lambda entry: get_instant_or_fn(entry.filename))
                    for entry in entries:
                        if entry.is_dir():
                            continue
                        if not path_is_timestream_file(entry.filename, extensions=self.format):
                            continue
                        if self.timefilter is not None and not self.timefilter.partial_within(op.basename(entry.filename)):
                            continue
                        self._files[op.basename(entry.filename)] = ZipContentFetcher(path, entry.filename)
                        yield TimestreamFile(filename=entry.filename,
                                             fetcher=ZipContentFetcher(path, entry.filename))
            elif tarfile.is_tarfile(path):
                self.sorted = False
                # warnings.warn("Extracting files from a tar file. Sorted iteration is not guaranteed")
                with tarfile.TarFile(path) as tar:
                    for entry in tar:
                        if not entry.isfile():
                            continue
                        if not path_is_timestream_file(entry.name, extensions=self.format):
                            continue
                        if self.timefilter is not None and not self.timefilter.partial_within(op.basename(entry.name)):
                            continue
                        if tar_contents:
                            filebytes = tar.extractfile(entry).read()
                            yield TimestreamFile.from_bytes(filebytes, filename=entry.name)
                        else:
                            self._files[op.basename(entry.name)] = TarContentFetcher(path, entry.name)
                            yield TimestreamFile(filename=entry.name,
                                                 fetcher=TarContentFetcher(path, entry.name))
            else:
                raise ValueError(f"'{path}' appears not to be an archive")

        def is_archive(path):
            if op.isdir(path):
                return False
            return op.exists(path) and op.isfile(path) and \
                (zipfile.is_zipfile(str(path)) or tarfile.is_tarfile(path))

        try:
            if is_archive(self.path):
                yield from walk_archive(self.path)
        except Exception as exc:
            print(f"\n{exc.__class__.__name__}: {str(exc)} at '{self.path}'\n", file=stderr)

        for root, dirs, files in os.walk(self.path):
            # ensure sorted iteration
            dirs.sort()
            files.sort(key=lambda f: get_instant_or_fn(f))
            for file in files:
                path = op.join(root, file)
                if file.startswith("."):
                    continue
                try:
                    if not (op.isfile(path) and os.access(path, os.R_OK)):
                        raise RuntimeError(f"Could not read {path}, skipping")
                    if is_archive(path):
                        if self.timefilter is not None and not self.timefilter.partial_within(file):
                            continue
                        yield from walk_archive(path)
                    if path_is_timestream_file(path, extensions=self.format):
                        if self.timefilter is not None and not self.timefilter.partial_within(file):
                            continue
                        fetcher = FileContentFetcher(path)
                        self._files[op.basename(path)] = fetcher
                        yield TimestreamFile(filename=op.basename(path), fetcher=fetcher)
                except Exception as exc:
                    print(f"\n{exc.__class__.__name__}: {str(exc)} at '{path}'\n", file=stderr)

    def _timestream_path(self, file):
        """Gets path for timestream file."""
        idxstr = ""
        if file.instant.index is not None:
            idxstr = "_" + str(file.instant.index)
        if self.add_subsecond_field:
            idxstr = "_00" + idxstr
        fname = f"{self.name}_%Y_%m_%d_%H_%M_%S{idxstr}.{file.format}"
        if self.flat_output:
            path = fname
        else:
            path = f"%Y/%Y_%m/%Y_%m_%d/%Y_%m_%d_%H/{fname}"
        return file.instant.datetime.strftime(path)

    def _bundle_archive_path(self, file):
        if self.bundle == "none":
            return None
        if self.bundle == "root":
            return f"{self.path}.{file.format}.zip"
        elif self.bundle == "year":
            bpath = f"{self.path}/{self.name}_%Y.{file.format}.zip"
        elif self.bundle == "month":
            bpath = f"{self.path}/%Y/{self.name}_%Y_%m.{file.format}.zip"
        elif self.bundle == "day":
            bpath = f"{self.path}/%Y/%Y_%m/{self.name}_%Y_%m_%d.{file.format}.zip"
        elif self.bundle == "hour":
            bpath = f"{self.path}/%Y/%Y_%m/%Y_%m_%d/{self.name}_%Y_%m_%d_%H.{file.format}.zip"
        elif self.bundle == "minute":
            bpath = f"{self.path}/%Y/%Y_%m/%Y_%m_%d/%Y_%m_%d_%H/{self.name}_%Y_%m_%d_%H_%M.{file.format}.zip"
        elif self.bundle == "second":
            bpath = f"{self.path}/%Y/%Y_%m/%Y_%m_%d/%Y_%m_%d_%H/{self.name}_%Y_%m_%d_%H_%M_%S.{file.format}.zip"
        return file.instant.datetime.strftime(bpath)

    def write(self, file):
        """ Adds a file to this timestream.

        :param file: A valid file for this timestream
        :type file: :class:`.TimestreamFile`
        """
        if op.exists(self._index_file):
            with FileLock(self._index_file):
                try:
                    os.unlink(self._index_file)
                except Exception as exc:
                    print(str(exc), file=stderr)
                    if stderr.isatty():
                        traceback.print_exc(file=stderr)
        if self.name is None:
            raise RuntimeError("TSv2Stream not opened")
        if not isinstance(file, TimestreamFile):
            raise TypeError("file should be a TimestreamFile")
        subpath = self._timestream_path(file)
        if self.bundle == "none":
            outpath = op.join(self.path, subpath)
            os.makedirs(op.dirname(outpath), exist_ok=True)
            with FileLock(outpath):
                with open(outpath, 'wb') as fh:
                    fh.write(file.content)
        else:
            if self.bundle == "root":
                self.path = str(self.path)
                for ext in [".tar", ".zip", f".{file.format}"]:
                    if self.path.lower().endswith(ext):
                        self.path = self.path[:-len(ext)]
                self.path = Path(self.path)
            bundle = self._bundle_archive_path(file)
            bdir = op.dirname(bundle)
            if bdir:  # i.e. if not $PWD
                os.makedirs(bdir, exist_ok=True)
            with FileLock(bundle):
                with zipfile.ZipFile(bundle, mode="a", compression=zipfile.ZIP_STORED,
                                     allowZip64=True) as zip:
                    pathinzip = op.join(self.name, subpath)
                    if pathinzip not in zip.namelist():
                        zip.writestr(pathinzip, file.content)
                    else:
                        file_crc = zlib.crc32(file.content)
                        zip_crc = zip.getinfo(pathinzip).CRC
                        if file_crc != zip_crc:
                            raise RuntimeError(f"ERROR: trying to overwrite file with different content: zip={bundle}, subpath={subpath}")

    def __iter__(self):
        return self.iter()

    def close(self):
        """ Maintains interface as other objects with ``close()`` methods but does not currently need further actions.
        """
        pass
