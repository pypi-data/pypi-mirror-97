import argparse
import runpy
import sys

from . import __name__ as _MODULE_NAME


def _get_command() -> str:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Parse command-line arguments"
    )
    parser.add_argument(
        "command", help='The name of a command ("clean", "distribute", etc.)?'
    )
    arguments: argparse.Namespace = parser.parse_known_args()[0]
    sys.argv.remove(arguments.command)
    return arguments.command


def main(command: str = "") -> None:
    """
    Run a sub-module corresponding to the indicated `operation`.

    Parameters:

    - command (str): The name of a sub-module to run as "__main__".
    """
    command = command or _get_command()
    module_name: str = f"{_MODULE_NAME}.{command}"
    runpy.run_module(module_name, run_name="__main__")


if __name__ == "__main__":
    main()
