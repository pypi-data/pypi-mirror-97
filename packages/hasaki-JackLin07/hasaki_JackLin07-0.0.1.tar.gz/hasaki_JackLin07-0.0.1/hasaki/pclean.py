import argparse
import subprocess
import os


def add_arguments(parser: argparse.ArgumentParser) -> None:
    pass

def run(options: argparse.Namespace) -> int:
    subprocess.call("ninja -t clean",env = os.environ.copy())
    return 0