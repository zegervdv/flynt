""" Test str processors on actual file contents """
import os
import pytest
import config
from fstringify.process import fstringify_code_by_line


int_test_dir = os.path.join(config.home, "test/integration/")

in_dir = os.path.join(int_test_dir, "samples_in")
out_dir = os.path.join(int_test_dir, "actual_out")
expected_dir = os.path.join(int_test_dir, "expected_out")

os.makedirs(out_dir, exist_ok=True)


def read_in(name):
    filepath = os.path.join(in_dir, name)
    with open(filepath) as f:
        txt = f.read()

    return txt

def read_expected(name):
    filepath = os.path.join(expected_dir, name)
    with open(filepath) as f:
        txt = f.read()

    return txt

def write_output_file(name, txt):
    filepath = os.path.join(out_dir, name)
    with open(filepath, 'w') as f:
        f.write(txt)

def try_on_file(filename: str):
    """ Given a file name (something.py) find this file in test/integration/samples_in,
    run flint_str on its content, write result to test/integration/actual_out/something.py,
    and compare the result with test/integration/expected_out/something.py"""
    txt_in = read_in(filename)
    out, edits = fstringify_code_by_line(txt_in)

    write_output_file(filename, out)
    return out, read_expected(filename)


test_files = list(sorted(os.listdir(in_dir)))
@pytest.fixture(params=["no_fstring_1.py",
                        "no_fstring_2.py",
                        "simple.py",
                        "simple_indent.py",
                        "simple_start.py",
                        "simple_comment.py",
                        "simple_docstring.py",
                        "simple_format.py",
                        "simple_percent.py",
                        "simple_percent_comment.py",
                        "multiple.py",
                        "some_named.py",
                        "all_named.py",
                        "first_string.py",
                        "named_inverse.py",
                        "def_empty_line.py",
                        "CantAffordActiveException.py",
                        "multiline.py",
                        "long.py"])
# @pytest.fixture(params=["first_string.py"])
def filename(request):
    yield request.param

def test_fstringify(filename):
    out, expected = try_on_file(filename)
    assert out == expected