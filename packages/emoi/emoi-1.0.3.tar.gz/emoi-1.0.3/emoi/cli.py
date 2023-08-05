import click
import sys

from . import __version__

from trobz.utils import generate_error_id


@click.command()
@click.option(
    "-V", "--version", is_flag=True, default=False, help="Show version and exit"
)
def main(version):
    if version:
        print("Version: {}".format(__version__))
        sys.exit(0)

    print(
        "Hi there fellow Trobzer :-)\n"
        "Please join #tech-support on Slack and post this error id: {}\n"
        "Thank you!".format(generate_error_id())
    )
    sys.exit(-1)
