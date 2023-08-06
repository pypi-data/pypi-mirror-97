import logging
import subprocess
import sys
import os
import json
import re
import uuid
import io
import gzip
from pathlib import Path
from . import insight


def _get_logger(level="INFO"):
    level = {
        "ERROR": logging.ERROR,
        "WARN": logging.WARN,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }[level]

    formatter = logging.Formatter(
        fmt="%(asctime)s — %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def _validate_base_directory():
    if not (Path.cwd() / "idk.json").exists():
        sys.exit(
            "No idk.json in current working directory, are you in the base directory of your insight?")


def _lint_directory(logger):
    has_error = False
    cwd = Path.cwd()
    # if not _correct_classname(cwd, logger):
    #     has_error = True

    for path in cwd.glob("**"):
        relative_path = path.relative_to(cwd)
        if not _is_hidden(relative_path):
            type_hint_cmd = f'mypy --ignore-missing-imports {relative_path}'
            for return_path in _execute_iterator(type_hint_cmd):
                if "error" in return_path and not "source file" in return_path:
                    has_error = True
                    logger.error(return_path)
    _check_methods()
    return has_error


def _check_methods():  # Check they've got the right methods on their class
    return None

# TODO CHECK for subclass
# def _correct_classname(cwd, logger):
#     with open("idk.json", "r") as config_file:
#         config = json.load(config_file)
#         print(f"The path is {Path.cwd()}")
#         sys.path.insert(0, str(Path.cwd()))
#         try:
#             cls = __import__(config["insight_file"].replace('.py', ''),
#                              fromlist=[config["insight_class"]])
#         except Exception as e:
#             logger.error(
#                 f"Couldn't import {config['insight_class']} from {config['insight_file']}:\n"
#             )
#             raise e

#         cls = getattr(cls, config['insight_class'])

#         if not issubclass(cls, insight.InsightGenerator):
#             logger.error(
#                 f"{config['insight_class']} must be a subclass of \"idk.insight.InsightGenerator\""
#             )
#             return False
#     return True


def run_cmd(cmd, **kwargs):
    try:
        output = subprocess.check_output(cmd, shell=True, **kwargs)
    except subprocess.CalledProcessError as e:
        print(f'{cmd}: CREATED ERROR')
        print(str(e.output, encoding='UTF-8'))
        sys.exit(e.returncode)
    return str(output, encoding='UTF-8')


def _execute_iterator(cmd, err_out=False):
    popen = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line.strip()
    popen.stdout.close()
    return_code = popen.wait()
    if return_code and err_out:
        print(err_out)
        raise subprocess.CalledProcessError(return_code, cmd)


def _get_insight_name():
    # Regex extract alphabeticals and stick them back together snake case
    words = re.findall("[a-zA-Z]+", Path.cwd().name)
    return "_".join(word.lower() for word in words)


def _get_create_hashname():
    cwd = Path.cwd()
    out_path = cwd / ".idk.out" / "out.json"

    if out_path.exists():
        # Check if hashname in file
        with open(out_path, "r") as out_file:
            out = json.load(out_file)
            if "hashname" in out:
                return out["hashname"]

        # If not then make one
        with open(cwd / "idk.json", "r") as config:
            config = json.load(config)
            out["hashname"] = config["insight_name"] + str(uuid.uuid4().hex)

        with open(out_path, "w") as out_file:
            out_file.write(json.dumps(out, indent=4))

    else:  # if no outfile exists
        with open(cwd / "idk.json", "r") as config:
            config = json.load(config)

        out = {"hashname": config["insight_name"] + str(uuid.uuid4().hex)}

        with open(out_path, "w+") as out_file:
            out_file.write(json.dumps(out, indent=4))

    return out["hashname"]


def _gzip_dir(cwd):
    """This function finds all the non-hidden files and folders, reads
    and stores them in a dict, encodes them into bytes, and gzip compresses
    them together to be sent.

    Args:
        cwd (str): current working directory
    """
    data = {}
    # Find paths+files
    cwd = Path.cwd()
    for path in cwd.glob("**"):
        relative_path = path.relative_to(cwd)
        if not _is_hidden(path):
            with open(relative_path, "r") as f:
                data[relative_path.as_posix()] = f.read()
    print(json.dumps(data, indent=4))
    # compressed = io.BytesIO()
    # with gzip.GzipFile(fileobj=compressed)


def _is_hidden(path):
    """Checks whether a file is hidden or in a hidden directory"""
    for part in path.as_posix().split("/"):
        if part.startswith("."):
            return True
    return False


def _get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def _in_virtualenv():
    return "VIRTUAL_ENV" in os.environ or _get_base_prefix_compat() != sys.prefix