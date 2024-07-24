import pytest
import pathlib
import logging
import subprocess


python_files = [
    f
    for f in pathlib.Path("docs").glob("**/code_reviews/**/*.py")
    if f.name != "__init__.py"
]


@pytest.mark.parametrize("fpath", python_files, ids=str)
def test_run_script(fpath):
    try:
        result = subprocess.run(
            ["python", fpath],
            capture_output=True,
            text=True,
            input="Hi\nexit\n",
            check=True,
        )

        logging.info(result.stdout)

    except subprocess.CalledProcessError as e:
        logging.error(e.stderr)
        raise AssertionError(f"Script {fpath} failed with error:\n{e.stderr}")
