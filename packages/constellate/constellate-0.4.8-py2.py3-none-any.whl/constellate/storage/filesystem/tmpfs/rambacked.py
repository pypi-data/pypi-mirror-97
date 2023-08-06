from memory_tempfile import MemoryTempfile
import tempfile
import os


def mkd_tmpfs(prefix=None, suffix=None, dir=None):
    """
    Create a temporary directory, preferably RAM back, for speed
    @return tempfile.TemporaryDirectory
    """
    tmpfs_dir = os.environ.get("TMPFS_DIR", None)
    additional_paths = [tmpfs_dir] if tmpfs_dir is not None else []
    temp = MemoryTempfile(additional_paths=additional_paths, fallback=True)
    if not hasattr(temp, "tempdir"):
        # Bug: memory_tempfile does not set the temp.tempdir attribute on non Linux OSes
        # Attribute set manually as a workaround until the library is
        # eventually fixed
        setattr(temp, "tempdir", tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=dir))
    return temp.TemporaryDirectory(prefix=prefix, suffix=suffix, dir=dir)


def mkd_tmp(prefix=None, suffix=None, dir=None):
    return tempfile.TemporaryDirectory(prefix=prefix, suffix=suffix, dir=dir)
