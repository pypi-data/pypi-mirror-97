# Copyright (c) 2018-2021 Kevin Murray <foss@kdmurray.id.au>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from tqdm import tqdm
import msgpack

import copy
from collections import defaultdict
import csv
from concurrent.futures import as_completed, ProcessPoolExecutor
from os import path as op
import re
from sys import stderr, stdout, stdin
import traceback
import warnings
import gc

csv.register_dialect('tsv',
                     delimiter='\t',
                     doublequote=False,
                     escapechar='\\',
                     lineterminator='\n',
                     quotechar='"',
                     quoting=csv.QUOTE_NONNUMERIC)


class FatalPipelineError(Exception):
    """Thrown for errors stopping the pipeline for all images (compare with :py:exc:`.AbortPipelineForThisImage`)."""
    pass


class AbortPipelineForThisImage(Exception):
    """Thrown for errors stopping the pipeline for the current image being processed only."""
    pass

def indent(text, by=2):
    res = []
    for line in text.split("\n"):
        res.append(" " * by + line)
    return "\n".join(res)


class TSPipeline(object):
    """
    Core TimeStream pipeline runner.
    """
    def __init__(self, *args, reporter=None):
        r"""
        :param \*args: Pipeline steps to execute
        :type \*args: :class:`.PipelineStep`
        :param reporter: Object to hold reports
        :type reporter: :class:`.ResultRecorder`
        """
        self.retcode = 0
        self.n = 0
        self.steps = []
        for step in args:
            self.add_step(step)
        if reporter is None:
            reporter = ResultRecorder()
        self.report = reporter

    def add_step(self, step):
        """Appends steps to this pipeline.

        :param step: Step to add.
        :type step: :class:`.PipelineStep`
        :return: self (adding steps can be chained)
        :rtype: :class:`.TSPipeline`
        """
        if not hasattr(step, "process_file"):
            raise ValueError(f"step doesn't seem to be a pipeline step: {step}")
        self.steps.append(step)
        return self  # so one can chain calls

    def process_file(self, file):
        """Processes all steps in current object.
        Mirrors :class:`.PipelineStep`, so an entire pipeline can function as a pipeline step.
        """
        for step in self.steps:
            file.report["Errors"] = None
            try:
                file = step.process_file(file)
                assert file is not None
            except AbortPipelineForThisImage as exc:
                file.report.update({"PipelineAbortedMessage": str(exc)})
                print(f"\nAborting at {step.__class__.__name__}: {str(exc)}", file=stderr)
                break
            except Exception as exc:
                path = file.filename
                if hasattr(file.fetcher, "pathondisk"):
                    path = file.fetcher.pathondisk
                print(f"\n{exc.__class__.__name__}: {str(exc)} while processing '{path}'\n", file=stderr)
                if stderr.isatty():
                    traceback.print_exc(file=stderr)
                file.report["Errors"] = f"{exc.__class__.__name__}: {str(exc)}"
                self.report.record(file.instant, **file.report)
                if isinstance(exc, FatalPipelineError):
                    raise
        self.report.record(file.instant, **file.report)
        return file

    def process(self, input_stream, ncpus=1, progress=True):
        """
        Processes files.

        :param input_stream: Timestream of files to process with pipeline.
        :type input_stream: :class:`pyts2.timestream.TimeStream`
        :param ncpus: Number of threads to use (default 1)
        :type ncpus: int
        :param progress: Unimplemented
        :type progress: bool
        """
        try:
            if ncpus > 1:
                with ProcessPoolExecutor(max_workers=ncpus) as executor:
                    for file in tqdm(executor.map(self.process_file, input_stream), unit=" files"):
                        if file is None:
                            continue
                        self.report.record(file.instant, **file.report)
                        self.n += 1
                        yield file
            else:
                for file in tqdm(input_stream, unit=" files"):
                    file = self.process_file(file)
                    if file is None:
                        continue
                    self.report.record(file.instant, **file.report)
                    self.n += 1
                    yield file
        except FatalPipelineError as exc:
            print(f"Apologies, we encountered a fatal pipeline error, and are stopping processing. The error is:\n{str(exc)}", file=stderr)
            self.retcode=1

    def __call__(self, *args, **kwargs):
        yield from self.process(*args, **kwargs)

    def process_to(self, input_stream, output, ncpus=1):
        for done in self.process(input_stream, ncpus=ncpus):
            output.write(done)

    def write(self, file):
        # TODO needed so that pipelines can be used as files
        pass

    def read(self, file):
        # TODO needed so that pipelines can be used as files
        pass

    def finish(self):
        """Calls finishing method for each PipelineStep and closes out reporting."""
        for step in self.steps:
            step.finish()
            if hasattr(step, "report") and isinstance(step.report, ResultRecorder):
                self.report.merge(step.report)
                step.report.close()
        self.report.close()

    def __repr__(self):
        out = ["TSPipeline:", ]
        for step in self.steps:
            out.append(indent(repr(step)))
        return "\n".join(out)


class ResultRecorder(object):
    """
    Saves pipeline data to a TSV file. Usually used with
    :class:`.ResultRecorderStep`, where the file path is specified.
    """
    def __init__(self):
        self.fields = []
        self.data = defaultdict(dict)

    def record(self, instant, **kwargs):
        for key, val in kwargs.items():
            if key not in self.fields:
                self.fields.append(key)
            self.data[repr(instant)].update(kwargs.copy())

    def merge(self, reporter):
        for inst, data in reporter.data.items():
            for key in data:
                if key not in self.fields:
                    self.fields.append(key)
            self.data[inst].update(data)

    def save(self, outpath, delim="\t"):
        if len(self.data) < 1:
            # No data, don't make file
            return
        with open(outpath, "w") as fh:
            tsvw = csv.writer(fh, dialect='tsv')
            tsvw.writerow(["Instant"] + self.fields)
            for instant, record in sorted(self.data.items()):
                line = [instant, ]
                for field in self.fields:
                    val = record.get(field, None)
                    if val is None:
                        val = "NA"
                    if isinstance(val, str):
                        val = re.sub(r"\s+", " ", val, re.IGNORECASE | re.MULTILINE)
                    line.append(val)
                tsvw.writerow(line)

    def close(self):
        pass


class LiveResultRecorder(ResultRecorder):
    """
    Writes results to file in a streaming log as soon as results are sent to it.
    (compare with :class:`.ResultRecorder`, which stores results and writes them later in a TSV)
    Unlike :class:`.ResultRecorder`, records file path is determined on init.
    """
    def __init__(self, fileorpath):
        """
        :param fileorpath: Writable file handle or path to records file
        :type fileorpath: :class:`io.TextIOWrapper` or str
        """
        if hasattr(fileorpath, "write"):
            self.file = fileorpath
        else:
            self.file = open(fileorpath)

    def record(self, instant, **kwargs):
        dat = {"instant": repr(instant)}
        dat.update(kwargs)
        self.file.write(msgpack.packb(dat))

    def merge(self, reporter):
        for inst, data in reporter.data.items():
            self.record(inst, **data)

    def close(self):
        self.file.close()

    def save(self):
        pass


##########################################################################################
#                                     Pipeline steps                                     #
##########################################################################################


class PipelineStep(object):
    """A generic base class for pipeline steps.

    All pipeline steps should implement a method called ``process_file`` that accepts one
    argument ``file``, and returns either :class:`pyts2.timestream.TimestreamFile` or a subclass of it.
    """

    def process_file(self, file):
        return file

    def finish(self):
        pass

    def __repr__(self):
        return self.__class__.__name__


class ResultRecorderStep(PipelineStep):
    """
    Writes out pipeline results at regular intervals.
    """

    def __init__(self, output_file):
        """
        :param output_file: Path to output TSV file
        :type output_file: str
        """
        self.n = 0
        self.output_file = output_file
        self.report = ResultRecorder()
        self.write_interval = 1000  # write results every write_interval images

    def process_file(self, file):
        self.report.record(file.instant, **file.report)
        self.n += 1
        if self.n % self.write_interval == 0:
            self.report.save(self.output_file)

    def finish(self):
        self.report.save(self.output_file)


class TeeStep(PipelineStep):
    """Execute another step or pipeline with no side effects on each ``file``"""

    def __init__(self, other_pipeline):
        """
        :param other_pipeline: Pipeline to process this file, branching off from this point
        :type other_pipeline: :class:`pyts2.timestream.TimestreamFile`
        """
        self.pipe = other_pipeline

    def process_file(self, file):
        self.pipe.process_file(copy.deepcopy(file))
        return file

    def __repr__(self):
        return "TeeStep:\n" + indent(repr(self.pipe))


class WriteFileStep(PipelineStep):
    """Write each file to output, without changing the file"""

    def __init__(self, output):
        """
        :param output: Writable Timestream instance
        :type output: :class:`.TimeStream`
        """
        self.output = output

    def process_file(self, file):
        self.output.write(file)
        return file


class FileStatsStep(PipelineStep):
    """Reports file name and size."""
    def process_file(self, file):
        file.report.update({"FileName": op.basename(file.filename),
                            "FileSize": len(file.content)})
        return file


class FilterStep(PipelineStep):
    """Filter out files from the rest of a pipeline based on a callback function."""
    def __init__(self, callback, message="Filter excluded image"):
        """
        :param callback: Callback function that accepts file as argument and returns true to continue the pipeline and false otherwise.
        :type callback: function
        :param message: Reason for filtering file (added to exception logging)
        :type message: str, optional
        :raises AbortPipelineForThisImage: When file is excluded
        """
        self.callback = callback
        self.message = message

    def process_file(self, file):
        if not self.callback(file):
            raise AbortPipelineForThisImage(self.message)
        return file


class ConditionalStep(PipelineStep):
    """Runs a step only if some conditional callback evaluates for an image.

    Useful for e.g. conditionally writing an image:

        pipeline.add_step(ConditionalStep(lambda im: im.pixels.sum() > 100, WriteFileStep(output)))

    will write only images whose sum of all pixel values is greater than 100.
    """
    def __init__(self, conditional_callback, step):
        """
        :param conditional_callback: Callback function that accepts file as argument and returns true to continue the pipeline and false otherwise.
        :type conditional_callback: function
        :param step: PipelineStep to run if conditional_callback evaultates to truthy
        :type step: PipelineStep
        """
        self.callback = conditional_callback
        self.step = step

    def process_file(self, file):
        if not self.callback(file):
            return file
        return self.step.process_file(file)

    def finish(self):
        self.step.finish()

    def __repr__(self):
        return self.__class__.__name__ + "\n" + indent(repr(self.step))


class ClearFileObjectStep(PipelineStep):
    """A helper to remove memory-consuming members of TSFile/TSImage objects

    All but required at the end of pipelines when using parallelisation, to
    prevent e.g. pixel/file content data being pickeled to send back to the
    coordinating thread, which would significantly impact performance and hog
    CPU and memory.
    """
    def process_file(self, file):
        file._content = None
        if hasattr(file, "_pixels"):
            file._pixels = None
        gc.collect()
        return file
