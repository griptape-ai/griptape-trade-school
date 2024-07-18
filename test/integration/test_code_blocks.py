import io
import os
import pytest
import pathlib
import textwrap
import logging

from mktestdocs import check_md_file

from check_code_blocks import get_all_code_blocks, check_py_string

# @pytest.mark.parametrize('fpath', pathlib.Path("docs").glob("**/*.md"), ids=str)
# def test_files_good(fpath):
#     check_md_file(fpath=fpath)

all_code_blocks = get_all_code_blocks("docs/**/*.md")

print(f"CODE BLOCKS COUNT: {len(all_code_blocks)}")

@pytest.mark.parametrize("block", all_code_blocks, ids=[f["id"] for f in all_code_blocks])
def test_code_block(block, monkeypatch):
    # Send some stdin for tests that use the Chat util
    monkeypatch.setattr("sys.stdin", io.StringIO("Hi\nexit\n"))
    
    check_py_string(block["code"])