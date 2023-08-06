"""Run ChillBoss as a module."""

import logging

import click
from pyfiglet import figlet_format

from chillboss import __version__
from chillboss.mouse import Pointer

logger: logging.Logger = logging.getLogger("chillboss")


@click.command()
@click.option(
    "--verbose", is_flag=True, help="Flag argument which sets the log level to Debug."
)
@click.option(
    "--movement",
    type=click.Choice(["random", "square"], case_sensitive=False),
    default="random",
    help="`random` and `square` movements are accepted. Default set to `random`",
)
@click.option(
    "--length",
    type=int,
    default=None,
    help="Accepted for `square` type of movement. Default set to `None`.",
)
@click.option(
    "--sleeptime",
    type=int,
    default=30,
    help="Time to be taken till next movement. Default set to 30 seconds.",
)
@click.option(
    "--motiontime",
    type=int,
    default=0,
    help="Time consumption of pointer to move from present coordinates to the next coordinates. "
    "Default set to 0 seconds.",
)
def chill(
    motiontime: int, sleeptime: int, length: int, movement: str, verbose: bool
) -> None:
    """Start the movement of the mouse with the command line arguments passed by the user.

    Args:
        motiontime (int): Time to be taken to move consecutive coordinates of pointer.
        sleeptime (int): Time to sleep in between consecutive movements of pointer.
        length (int): Applicable for square movement, length of edge of square in pixels.
        movement (str): Type of movement, `square` and `random` are allowed. Default to `random`
        verbose (bool): Verbose the logs to debug level if True, else to Warning.

    Returns:
        None(None):

    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    pointer = Pointer(
        movement=movement, length=length, sleep_time=sleeptime, motion_time=motiontime
    )
    print(figlet_format("ChillBoss"))
    print(f"Version: {__version__}")
    pointer.move_the_mouse_pointer()


if __name__ == "__main__":
    chill()
