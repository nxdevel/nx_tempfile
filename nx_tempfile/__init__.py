"""A drop-in replacement for tempfile that adds the errors argument to
NamedTemporary and TemporaryFile.
"""
import os
import io
import tempfile
from tempfile import * # pylint: disable=wildcard-import, ungrouped-imports


__all__ = tempfile.__all__


def _patch_encoding(ctor, mode, **kwargs):
    "Wrap the resulting instance if the errors argument is provided"
    # The strategy is to create the underlying instance in binary mode and
    # wrap the result in a TextIOWrapper with the appropriate encoding/errors

    binary = 'b' in mode

    # If the <errors> argument was not passed or if the mode is not binary and
    # 'strict' was specifed, the default errors mode, then the default
    # implementation can be used
    errors = kwargs.pop('errors', None)
    if errors is None or not binary and errors == 'strict':
        return ctor(mode=mode, **kwargs)

    # Encoding/errors are only valid for text mode
    if binary:
        raise ValueError('binary mode doesn\'t take an errors argument')

    # Determine how the buffering should be handled
    buffering = kwargs.pop('buffering', -1)
    if buffering == 0:
        # A <buffering> of 0 is binary only
        raise ValueError('can\'t have unbuffered text I/O')

    if buffering == 1:
        # A <buffering> of 1 is line buffering - the binary instance will have
        # no buffering specified and the TextIOWrapper will have line buffering
        # enabled
        buffering = -1
        line_buffering = True
    else:
        # The <buffering> argument is not 0 or 1 so it will be passed directly
        # to the binary instance and the TextIOWrapper will have no line
        # buffering
        line_buffering = False

    encoding = kwargs.pop('encoding', None)
    newline = kwargs.pop('newline', None)
    fobj = ctor(mode=mode.replace('t', '') + 'b', buffering=buffering,
                encoding=None, newline=None, **kwargs)

    try:
        return io.TextIOWrapper(fobj, encoding=encoding, errors=errors,
                                newline=newline, line_buffering=line_buffering)
    except:
        fobj.close()

        # Attempt to clean up on exception if the object does not delete itself
        if not getattr(fobj, 'delete', True):
            os.unlink(fobj.name)

        raise


def TemporaryFile(mode='w+b', **kwargs): # pylint: disable=invalid-name, function-redefined
    "Wrapper around TemporaryFile to add errors argument."
    return _patch_encoding(tempfile.TemporaryFile, mode, **kwargs)


def NamedTemporaryFile(mode='w+b', **kwargs): # pylint: disable=invalid-name, function-redefined
    "Wrapper around NamedTemporaryFile to add errors argument."
    return _patch_encoding(tempfile.NamedTemporaryFile, mode, **kwargs)
