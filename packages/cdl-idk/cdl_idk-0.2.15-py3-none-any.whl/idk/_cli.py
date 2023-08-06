#! python3

import argparse
import io
import json
import os
import pprint
import re
import shutil
import sys
import uuid
import zipfile
import gzip
from pathlib import Path
import importlib.resources as pkg_resources
import requests

from ._service import _service_url
from ._utils import (
    _get_logger,
    _validate_base_directory,
    _lint_directory,
    _get_insight_name,
    _get_create_hashname,
    _gzip_dir,
    _execute_iterator,
    _in_virtualenv
)
from ._version import __version__
from . import templates
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

logger = _get_logger()


def _init():
    """method describes what happens when someone runs idk init in folder"""
    cwd = Path.cwd()
    # Check folder is empty
    if len(list(cwd.iterdir())) != 0:
        logger.error("A new insight can only be started in a empty directory.")
        sys.exit(1)
    # Check if folder name is short enough -
    # basically if it's smaller than the max size of insihgtg generator id - hash

    # Check folder name is alphabetical with addition of "-" "_"

    logger.info("Creating Insight directory structure...")
    insight_name = _get_insight_name()
    if len(insight_name) == 0:
        logger.error(
            "The alphabetical letters in your file is used to create your insight name. You need at least 1 letter."
        )
        sys.exit(1)

    insight_file = "{}.py".format(insight_name)
    class_name = insight_name.title().replace("_", "")

    # Make idk config json
    with open("idk.json", "w+") as config_file:
        config = {
            "insight_name": insight_name,
            "insight_file": insight_file,
            "insight_class": class_name
        }
        json.dump(config, config_file, indent=4)

    # Insight file
    with open(insight_file, "w+") as f:
        template = pkg_resources.read_text(templates, "_gen_template.py")
        f.write(template.replace("_DeveloperInsight_", class_name))

    # insight requirements
    with open("requirements.txt", "w+") as req:
        req.writelines([
            "# Add your main insight requirements here, transcription function and tracking function requirements can be specifiec in their respective folders.",
            "You can add the packages in your currrent python environemnt with:\n",
            "#     `pip freeze > requirements.txt`\n",
            f"idk=={__version__}",
        ]
        )

    # Transcription Folder
    transcip_dir = Path.cwd() / "transcription"
    Path.mkdir(transcip_dir)
    with open(transcip_dir / "transcribe.py", "w+") as f:
        template = pkg_resources.read_text(templates, "_trans_template.py")
        f.write(template.replace("_DeveloperInsight_", class_name))

    with open(transcip_dir / "requirements.transcription.txt", "w+") as f:
        f.writelines(
            ["# This is where you can write the required pip installs for your transcription function"])

    # Tracking Folder
    tracking_dir = Path.cwd() / "tracking"
    Path.mkdir(tracking_dir)
    with open(tracking_dir / "tracking.py", "w+") as f:
        template = pkg_resources.read_text(templates, "_tracking_template.py")
        f.write(template.replace("_DeveloperInsight_", class_name))

    with open(tracking_dir / "requirements.tracking.txt", "w+") as f:
        f.writelines(
            ["# This is where you can write the required pip installs for your tracking functions"])

    if not _in_virtualenv():  # in venv -> True
        for output in _execute_iterator("python3 -m venv .venv"):
            logger.info(output)

        logger.info(
            "READY! You can activate your virtual environment with 'source ./.venv/bin/activate'. Happy coding!")
    else:
        logger.info(
            "Active virtual environment detected; skipping virtual env creation!")
        logger.info("READY!")


def _deploy(test):
    """Define What happends when someone runs idk deploy in a folder
    """
    has_error = _lint_directory(logger)
    if has_error:
        logger.error("Please fix the above errors before deploying.")
        sys.exit(1)

    _validate_base_directory()
    # Check and make output dir
    outdir = Path.cwd() / ".idk.out"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    _get_create_hashname()
    # hashname = _get_create_hashname()

    # compressd_dir = _gzip_dir(cwd)
    # sys.exit(0)

    # Upload to cloud
    # ------------------
    # Can get user credential from:
    # os.path.expanduser("~") + /.idk/crednetials?
    # with open(zip_path, "rb") as outfile:

    #     params = {"hashname": hashname}
    #     compressed = io.BytesIO()
    #     with gzip.GzipFile(fileobj=compressed, mode="w") as gz:
    #         json_data = json.dumps({"zfile": outfile.read()})

    #     print(outfile.read())
    #     # headers = {'Content-type': 'application/zip'}
    #     with requests.post(
    #         _service_url + "insight",
    #         params=params,
    #         data=# headers=headers
    #     ) as response:
    #         if response.ok:
    #             logger.info("Success! Your insight is deployed to the insight engine! Deploy again to update.\n" +
    #                         json.dumps(json.loads(response.content), indent=4)
    #                         )
    #         else:
    #             logger.error("Unable to deploy your insight:\n" +
    #                          json.dumps(json.loads(response.content), indent=4)
    #                          )


def _destroy(test):
    """Code that runs when a user wants to delete their insight.
    """
    _validate_base_directory()

    # with requests.delete(_service_url + "insight", params={"hashname": _get_hashname()}) as response:
    #     print(json.loads(response.content))

    # When we destroy we will need to delete the hashkey in order to make a new one next time it's deployed?
    # Probably yes for safety reasons (no risk of accidentally not deleting a lambda functions somewhere and)
    # THIS SHOULD DEFINITELY ONLY RUN IF WE'RE SURE ALL THE OTHER SERVICES HASVE DELETED THEIR PARTS.

    # WE WANT TO ARCHIVE OLD RESOURCES RATHER THAN DELETE THEM AS WE'RE STILL OGNNA HAVE PAYLOADS WITH THAT GENERATOR ID
    shutil.rmtree(Path.cwd() / ".idk.out")


def main():
    parser = argparse.ArgumentParser(
        prog="CDL Insights Development Kit (cdl_idk)",
        description="A toolkit to help you build and deploy impactful insights for the CDL Insights Engine."
    )
    parser.add_argument("--init", action="store_true",
                        help="creates a new insight project in the current empty directory")
    parser.add_argument("--deploy", action="store_true",
                        help="deploys or updates your insight to CDL Insights Engine")
    parser.add_argument("--destroy", action="store_true",
                        help="tears down you insight from CDL Insight Engine")
    parser.add_argument("-t", "--test", action="store_true",
                        help="for developer use only")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    args = parser.parse_args()
    if args.init:
        if args.test:
            logger.warning("test flag has no affect on init command")
        _init()
    elif args.deploy:
        _deploy(args.test)
    elif args.destroy:
        _destroy(args.test)
    else:
        logger.error("Please pass one of init, deploy, or destroy arguments.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
