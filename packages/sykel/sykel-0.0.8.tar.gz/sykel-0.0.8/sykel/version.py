"""
 
 This module use bumpversion for handling versioning.
 
"""

import os
import configparser
from invoke import run, task

CONFIG_FILEPATH = "setup.cfg"
FILE_TO_SEARCH_TEMPL = "bumpversion:file:{filepath}"


def init():
    config = configparser.ConfigParser()
    
    config["bumpversion"] = dict(
        current_version="0.0.1",
        commit=True,
        tag=True)
    
    config[FILE_TO_SEARCH_TEMPL.format(filepath=CONFIG_FILEPATH)] = dict()
    
    with open(CONFIG_FILEPATH, "w") as config_file:
        config.write(config_file)


def bump(part: str):
    cmd = "bumpversion{config_file} --allow-dirty {part}".format(
        # NOTE: Need this to convince bumpversion to work with setup.cfg it seems.
        # Has been observed at least in one case, but might not always be so.
        config_file=" --config-file %s" % CONFIG_FILEPATH if os.path.exists(CONFIG_FILEPATH) else "",
        part=part)
    run(cmd, echo=True)
    push = input("\nPush version tags (y/n)? ")
    if push == 'y':
        run('git push && git push --tags')
    else:
        print("Remember to do 'git push && git push --tags' to push version tags.")


def add_file(filepath: str):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILEPATH)
    config[FILE_TO_SEARCH_TEMPL.format(filepath=filepath)] = dict()
    with open(CONFIG_FILEPATH, "w") as config_file:
        config.write(config_file)


@task(name="init")
def init_tsk(ctxt):
    """
    Initialize bumpversion configuration
    """
    init()


@task(name="bump")
def bump_tsk(ctxt, part="patch"):
    """
    Bump version: [--part <major, minor, [patch]>]
    
    Part can be either one of: major | minor | patch (default)
    """
    bump(part)


@task(name="add_file")
def add_file_tsk(ctxt, filepath):
    """
    Add file to that should have version updated: --filepath <>
    """
    add_file(filepath)
