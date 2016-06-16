A drop-in replacement for tempfile with wrappers to correct some issues.

All functions/classes from tempfile are pulled into __init__.

TemporaryFile and NamedTemporaryFile do not take an errors argument to pass on
to the underlying _open() so they are wrapped in this implementation.

Note: no wrapper for SpooledTemporaryFile is currently provided as the
reference implementation doesn't encode until after rollover.
