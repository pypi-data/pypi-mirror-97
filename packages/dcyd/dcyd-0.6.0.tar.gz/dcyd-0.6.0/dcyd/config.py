import argparse
import json
import os
import pathlib
import pkgutil

import dcyd.utils.constants as constants

def args_parser():
    parser = argparse.ArgumentParser(description='Configure client to communicate with dcyd.')
    parser.add_argument(
        'project_id',
        metavar='DCYD_PROJECT_ID',
        default=os.getenv('DCYD_PROJECT_ID', None),
        nargs='?',
        help='alphanumeric project identifier (found in the web app)'
    )
    parser.add_argument(
        'project_access_token',
        metavar='DCYD_PROJECT_ACCESS_TOKEN',
        default=os.getenv('DCYD_PROJECT_ACCESS_TOKEN', None),
        nargs='?',
        help='alphanumeric project access token (found in the web app)'
    )
    parser.add_argument(
        '-o', '--output-file',
        dest='config_file',
        default=constants.CONFIG_FILE,
        help='output config file name (default: {})'.format(constants.CONFIG_FILE)
    )

    return parser


def configure_client(*, project_id, project_access_token, config_file):
    if not project_id: raise ValueError('project_id is required')
    if not project_access_token: raise ValueError('project_access_token is required')

    config_json = json.dumps({
        'project_id': project_id,
        'project_access_token': project_access_token,
    }, indent=2)
    pathlib.Path(config_file).write_text(config_json)


def main():
    """Calls the config service to get credentials."""

    ascii_art = pkgutil.get_data(__name__, "static/dcyd-ascii-art.txt").decode()
    print(ascii_art)

    parser = args_parser()
    args = parser.parse_args()
    project_id = args.project_id
    project_access_token = args.project_access_token
    config_file = args.config_file

    if project_id and project_access_token:
        configure_client(
            project_id=project_id,
            project_access_token=project_access_token,
            config_file=config_file,
        )
        print(f"Client config file `{config_file}` generated successfully.")
        print(f"As a final step, run `export DCYD_CONFIG_FILE={config_file}`.")
    else:
        parser.print_help()

