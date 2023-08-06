import contextlib


@contextlib.contextmanager
def no_context():
    """A Python 3.6-compatible version of contextlib.nullcontext"""
    yield
