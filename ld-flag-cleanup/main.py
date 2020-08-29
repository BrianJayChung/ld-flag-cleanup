import click
import click_log

import requests
import json
import os

from ld import LaunchDarklyApi
from util import create_file, read_file, move_file, LOG
from dotenv import load_dotenv

load_dotenv()

LD_API_KEY = os.getenv("LD_API_KEY")
LD_PROJ_KEY = os.getenv("LD_PROJ_KEY")
LD_ENV_KEY = os.getenv("LD_ENV_KEY")

LD_API = LaunchDarklyApi(
        LD_API_KEY,
        LD_PROJ_KEY,
        LD_ENV_KEY
    )

# set up logging
click_log.basic_config(LOG)

@click.group()
@click_log.simple_verbosity_option()
@click.version_option(prog_name='fcs')
@click.help_option()
def cli() -> None:
    """
    A CLI for cleaning up flag scripts
    """

@click.command()
def delete_flags():
    """
    Perform the delete action
    """
    # create_delete_list()

    list_of_flags, file_name = read_file()
    for flag in list_of_flags:
        delete_feature_flag(flag)
    move_file(file_name)


@click.command()
def create_delete_list():
    """
    find flags in Support-service not tagged with "real"
    """
    real_flags = get_real_flags()
    all_flags = get_all_flags()

    diff_flags = set(all_flags) - set(real_flags)
    create_file(diff_flags)

def get_real_flags():
    """
    Get flags tagged with real
    """
    return LD_API.get_flags(project_key="support-service", tag="real")

def get_all_flags():
    """
    Get all feature flags
    """
    return LD_API.get_flags(project_key="support-service")

def get_test_custom_roles():
    """
    Get custom roles with the word "test" in key
    """
    return LD_API.get_custom_roles()

def delete_feature_flag(flag):
    """
    delete flags
    """
    LD_API.delete_flag(project_key=LD_PROJ_KEY, feature_flag=flag)

cli.add_command(delete_flags)
cli.add_command(create_delete_list)

if __name__ == '__main__':
    cli()
