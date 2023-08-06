import os
import shutil
from sys import stdout, stderr, stdin, exit  # noqa
from os.path import dirname, basename, splitext, getsize, realpath
import click
from tqdm import tqdm
import traceback


class Removalist(object):
    """ Handles file removal.
    """
    def __init__(self, rm_script=None, mv_dest=None, force=False):
        """ Removes files, with the option to save a script for manual review,
        delete files immediately, or move each file to a trash directory.

        :param rm_script: Path to removal script. Does not save a script if ``None`` (default)
        :type rm_script: str, optional
        :param mv_dest: Path to move files to. Deletes files directly if ``None`` (default)
        :type mv_dest: str, optional
        :param force: Deletes/moves files without prompting. Not used if saving to removal script.
        :type force: bool, optional
        """
        self.force = force
        self.mv_dest = mv_dest
        self.to_delete = []

        self.rm_script = rm_script
        if self.rm_script is not None:
            with open(self.rm_script, "w") as fh:
                print("# rmscript", file=fh)

    def _do_delete(self):
        if self.rm_script is not None:
            with open(self.rm_script, "a") as fh:
                cmd = "rm -vf" if self.mv_dest is None else f"mv -n -t {self.mv_dest}"
                for f in self.to_delete:
                    print(cmd, realpath(f), file=fh)
        else:
            if not self.force:
                if self.mv_dest is not None:
                    click.echo(f"Will move the following files to {self.mv_dest}:")
                else:
                    click.echo("Will delete the following files:")
                for f in self.to_delete:
                    click.echo(f"\t{f}")
            if self.force or click.confirm("Is that OK?"):
                for f in self.to_delete:
                    try:
                        if self.mv_dest is None:
                            os.unlink(f)
                        else:
                            os.makedirs(self.mv_dest, exist_ok=True)
                            shutil.move(f, self.mv_dest)
                    except Exception as exc:
                        tqdm.write(f"Error deleting {f}: {str(exc)}")
                        if stderr.isatty():
                            traceback.print_exc(file=stderr)
                tqdm.write(f"Deleted {len(self.to_delete)} files")
        self.to_delete = []

    def remove(self, filepath):
        """ Based on options, either writes to a removal script, moves to
        another directory, or deletes file directly. Does not execute chosen
        action until object exits or more than 1000 files are queued.

        :param filepath: Path of file to remove.
        :type filepath: str
        :raises Exception: If set to delete directly, raises Exception if unable to delete file
        """
        if len(self.to_delete) > 1000:
            self._do_delete()
        self.to_delete.append(filepath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._do_delete()
