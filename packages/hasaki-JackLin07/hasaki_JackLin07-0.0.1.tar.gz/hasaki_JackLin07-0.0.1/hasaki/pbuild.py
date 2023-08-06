import argparse
import subprocess
import os



def check_config_file_is_update():
    pass


def add_arguments(parser: argparse.ArgumentParser) -> None:
    pass

def run(options: argparse.Namespace) -> int:
    ret_code = subprocess.call("ninja pretask_all",env = os.environ.copy())
    if ret_code == 1:
        return
    ret_code = subprocess.call("ninja all",env = os.environ.copy())
    if ret_code == 1:
        return
    ret_code =subprocess.call("ninja posttask_all",env = os.environ.copy())
    if ret_code == 1:
        return
    return 0



