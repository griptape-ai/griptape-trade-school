import io
import pytest
import pathlib
import logging

def check_py_string(source: str) -> None:
    """Exec the python source given in a new module namespace.

    Does not return anything, but exceptions raised by the source
    will propagate out unmodified
    """
    try:
        exec(source, {"__MODULE__": "__main__"})
    except Exception:
        logging.info(source)
        raise

@pytest.mark.parametrize('fpath', pathlib.Path("docs").glob("**/code_reviews/**/*.py"), ids=str)
def test_code_block(fpath, monkeypatch):
    # Send some stdin for tests that use the Chat util
    monkeypatch.setattr("sys.stdin", io.StringIO("Hi\nexit\n"))

    check_py_string(fpath.read_text())
    