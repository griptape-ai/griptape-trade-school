import io
import pytest
import pathlib
import logging
import subprocess


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


# @pytest.mark.parametrize('fpath', pathlib.Path("docs").glob("**/code_reviews/**/*.py"), ids=str)
# def test_code_block(fpath, monkeypatch):
#     # Send some stdin for tests that use the Chat util
#     monkeypatch.setattr("sys.stdin", io.StringIO("Hi\nexit\n"))

#     check_py_string(fpath.read_text())

python_files = [f for f in pathlib.Path("docs").glob("**/code_reviews/**/*.py") if f.name != "__init__.py"]


@pytest.mark.parametrize('fpath', python_files, ids=str)
def test_run_script(fpath):
    # Running the script and capturing the output
    result = subprocess.run(
        [
            "python",
            fpath,
        ],
        capture_output=True,
        text=True,
        input="Hi\nexit\n",
    )

    # Printing the output of the script
    print("Output of the script:")
    print(result.stdout)

    # Printing any error messages
    if result.stderr:
        print(result.stderr)
        raise Exception(result.stderr)
