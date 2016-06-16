# pylint: disable=missing-docstring, no-self-use, invalid-name
import os
import io
import codecs
import pytest
from nx_tempfile import NamedTemporaryFile, TemporaryFile


def reference(data, encoding, errors):
    "Round-trip the data according to the object encoding rules."
    with io.TextIOWrapper(io.BytesIO(), encoding=encoding,
                          errors=errors, newline='\n') as fobj:
        fobj.write(data)
        fobj.seek(0)
        return fobj.read()


class TestTemporaryFile:
    def test_pass_through_utf8(self):
        data = '12\u00d6\n'

        fobj = TemporaryFile('xt+', encoding='utf-8')
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        fobj = TemporaryFile('xt+', encoding='utf-8', errors=None)
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        fobj = TemporaryFile('xt+', encoding='utf-8', errors='strict')
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_pass_through_utf8_context(self):
        data = '12\u00d6\n'

        with TemporaryFile('xt+', encoding='utf-8') as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        with TemporaryFile('xt+', encoding='utf-8', errors=None) as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        with TemporaryFile('xt+', encoding='utf-8', errors='strict') as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_pass_through_ascii(self):
        data = '12\u00d6\n'

        fobj = TemporaryFile('xt+', encoding='ascii')
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        fobj = TemporaryFile('xt+', encoding='ascii', errors=None)
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        fobj = TemporaryFile('xt+', encoding='ascii', errors='strict')
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_pass_through_ascii_context(self):
        data = '12\u00d6\n'

        with TemporaryFile('xt+', encoding='ascii') as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        with TemporaryFile('xt+', encoding='ascii', errors=None) as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

        with TemporaryFile('xt+', encoding='ascii', errors='strict') as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_ignore(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        fobj = TemporaryFile('xt+', encoding='ascii', errors='ignore')
        assert fobj.closed is False
        assert fobj.line_buffering is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_ignore_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        with TemporaryFile('xt+', encoding='ascii', errors='ignore') as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_ignore_buffering(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        fobj = TemporaryFile('xt+', encoding='ascii', errors='ignore',
                             buffering=1)
        assert fobj.closed is False
        assert fobj.line_buffering is True
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_ignore_buffering_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        with TemporaryFile('xt+', encoding='ascii', errors='ignore',
                           buffering=1) as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is True
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_replace(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        fobj = TemporaryFile('xt+', encoding='ascii', errors='replace')
        assert fobj.closed is False
        assert fobj.line_buffering is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_replace_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        with TemporaryFile('xt+', encoding='ascii', errors='replace') as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_replace_buffering(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        fobj = TemporaryFile('xt+', encoding='ascii', errors='replace',
                             buffering=1)
        assert fobj.closed is False
        assert fobj.line_buffering is True
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_replace_buffering_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        with TemporaryFile('xt+', encoding='ascii', errors='replace',
                           buffering=1) as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is True
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert isinstance(fobj.name, int) or not os.path.exists(fobj.name)

    def test_binary_with_errors(self):
        with pytest.raises(ValueError):
            TemporaryFile('xb+', errors='ignore')

    def test_invalid_buffering(self):
        # <buffering> is passed to the underlying constructor without checking
        # unless <errors> is specified
        with pytest.raises(ValueError):
            TemporaryFile('xt', errors='ignore', buffering=0)

    def test_invalid_iowrap_fail(self):
        # A bit of cheating here as we know we can induce an error in the
        # text wrapper to ensure the final section of the __init__ gets tested
        encoding = 'xxxasciixxx'
        with pytest.raises(LookupError):
            codecs.lookup(encoding)
        with pytest.raises(LookupError):
            TemporaryFile('xt', encoding=encoding, errors='ignore')


class TestNamedTemporaryFile:
    def test_pass_through_utf8(self):
        data = '12\u00d6\n'

        fobj = NamedTemporaryFile('xt+', encoding='utf-8')
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='utf-8', errors=None)
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='utf-8', errors='strict')
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_pass_through_utf8_no_delete(self):
        data = '12\u00d6\n'

        fobj = NamedTemporaryFile('xt+', encoding='utf-8', delete=False)
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='utf-8', errors=None,
                                  delete=False)
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='utf-8', errors='strict',
                                  delete=False)
        assert fobj.closed is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == data
        fobj.close()
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

    def test_pass_through_utf8_context(self):
        data = '12\u00d6\n'

        with NamedTemporaryFile('xt+', encoding='utf-8') as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='utf-8', errors=None) as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='utf-8',
                                errors='strict') as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_pass_through_utf8_context_no_delete(self):
        data = '12\u00d6\n'

        with NamedTemporaryFile('xt+', encoding='utf-8', delete=False) as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='utf-8', errors=None,
                                delete=False) as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='utf-8', errors='strict',
                                delete=False) as fobj:
            assert fobj.closed is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == data
        assert fobj.closed is True
        assert os.path.exists(fobj.name)
        os.unlink(fobj.name)
        assert not os.path.exists(fobj.name)

    def test_pass_through_ascii(self):
        data = '12\u00d6\n'

        fobj = NamedTemporaryFile('xt+', encoding='ascii')
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors=None)
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors='strict')
        assert fobj.closed is False
        with pytest.raises(UnicodeEncodeError):
            fobj.write(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ''
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_pass_through_ascii_context(self):
        data = '12\u00d6\n'

        with NamedTemporaryFile('xt+', encoding='ascii') as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='ascii', errors=None) as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

        with NamedTemporaryFile('xt+', encoding='ascii',
                                errors='strict') as fobj:
            assert fobj.closed is False
            with pytest.raises(UnicodeEncodeError):
                fobj.write(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ''
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_ignore(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors='ignore')
        assert fobj.closed is False
        assert fobj.line_buffering is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_ignore_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        with NamedTemporaryFile('xt+', encoding='ascii',
                                errors='ignore') as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_ignore_buffering(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors='ignore',
                                  buffering=1)
        assert fobj.closed is False
        assert fobj.line_buffering is True
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_ignore_buffering_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='ignore')
        with NamedTemporaryFile('xt+', encoding='ascii', errors='ignore',
                                buffering=1) as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is True
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_replace(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors='replace')
        assert fobj.closed is False
        assert fobj.line_buffering is False
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_replace_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        with NamedTemporaryFile('xt+', encoding='ascii',
                                errors='replace') as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is False
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_replace_buffering(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        fobj = NamedTemporaryFile('xt+', encoding='ascii', errors='replace',
                                  buffering=1)
        assert fobj.closed is False
        assert fobj.line_buffering is True
        assert fobj.write(data) == len(data)
        assert fobj.seek(0) == 0
        assert fobj.read() == ref
        fobj.close()
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_replace_buffering_context(self):
        data = '12\u00d6\n'
        ref = reference(data, encoding='ascii', errors='replace')
        with NamedTemporaryFile('xt+', encoding='ascii', errors='replace',
                                buffering=1) as fobj:
            assert fobj.closed is False
            assert fobj.line_buffering is True
            assert fobj.write(data) == len(data)
            assert fobj.seek(0) == 0
            assert fobj.read() == ref
        assert fobj.closed is True
        assert not os.path.exists(fobj.name)

    def test_binary_with_errors(self):
        with pytest.raises(ValueError):
            NamedTemporaryFile('xb+', errors='ignore')

    def test_invalid_buffering(self):
        # <buffering> is passed to the underlying constructor without checking
        # unless <errors> is specified
        with pytest.raises(ValueError):
            NamedTemporaryFile('xt', errors='ignore', buffering=0)

    def test_invalid_iowrap_fail(self):
        # A bit of cheating here as we know we can induce an error in the
        # text wrapper to ensure the final section of the __init__ gets tested
        encoding = 'xxxasciixxx'
        with pytest.raises(LookupError):
            codecs.lookup(encoding)
        with pytest.raises(LookupError):
            NamedTemporaryFile('xt', encoding=encoding, errors='ignore',
                               delete=False)
