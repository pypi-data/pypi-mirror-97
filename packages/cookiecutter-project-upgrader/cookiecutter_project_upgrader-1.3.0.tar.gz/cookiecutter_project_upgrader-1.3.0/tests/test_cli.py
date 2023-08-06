from click.testing import CliRunner

from cookiecutter_project_upgrader.cli import main
from tests.tmp_files import CreateTempDirectory
from pathlib import Path
import subprocess


def invoke(arguments):
    runner = CliRunner()
    return runner.invoke(main, arguments)


def invoke_successful(arguments):
    result = invoke(arguments)

    if result.exit_code:
        raise result.exception


def invoke_failing(arguments):
    result = invoke(arguments)

    if not result.exit_code:
        raise RuntimeError("Unexpected success:\n{}".format(result.stdout))


def test_cli():
    invoke_successful(["--help"])

    invoke_failing(["--context-file", "./non-existing-file.py"])

    # Test non existing zip file
    invoke_failing(["--zip-file", "./non-existing-file.zip",
                    "--context-file", "dummy_cookiecutter_template/cookiecutter.json"])

    # Test bad existing zip file
    with CreateTempDirectory("testzip") as testdir:
        subprocess.run(["touch", "bad.zip"], cwd=Path(testdir), check=True)
        invoke_failing(["--zip-file", str(testdir.joinpath("bad.zip")),
                        "--context-file", "dummy_cookiecutter_template/cookiecutter.json"])

    # Test non existing http url zip file
    invoke_failing(["--zip-file", "http://test.com/non-existing-file.zip",
                    "--context-file", "dummy_cookiecutter_template/cookiecutter.json"])
