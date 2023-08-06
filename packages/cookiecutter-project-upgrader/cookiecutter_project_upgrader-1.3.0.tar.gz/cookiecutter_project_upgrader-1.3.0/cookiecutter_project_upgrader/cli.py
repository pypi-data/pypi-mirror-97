import click
import json
import os
from pathlib import Path
from typing import Optional, Tuple
from zipfile import ZipFile, BadZipFile

from cookiecutter_project_upgrader.logic import update_project_template_branch


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--context-file', '-c', type=click.Path(file_okay=True, readable=True, allow_dash=True),
              default="docs/cookiecutter_input.json", help="Default: docs/cookiecutter_input.json")
@click.option('--branch', '-b', default="cookiecutter-template", help="Default: cookiecutter-template")
@click.option('--upgrade-branch', '-u',
              help="Optional branch name of cookiecutter template to checkout before upgrading.")
@click.option('--zip-file', '-f', help="Zip file Path/URL for Cookiecutter templates.")
@click.option('--interactive', '-i', is_flag=True,
              help="Enter interactive mode. Default behaviour: skip questions, use defaults.")
@click.option('--merge-now', '-m', type=bool, default=None,
              help="Execute a git merge after a successful update, default: ask if interactive, otherwise false.")
@click.option('--push-template-branch-changes', '-p', type=bool, default=None,
              help="Push changes to the remote Git branch on a successful update, "
                   "default: ask if interactive, otherwise false.")
@click.option('--exclude', '-e', type=str, multiple=True,
              help='Git pathspecs to exclude from the update commit, e.g. -e "*.py" -e "tests/".')
def main(context_file: str, branch: str, upgrade_branch: Optional[str],
         zip_file: Optional[str], interactive: bool, merge_now: Optional[bool],
         push_template_branch_changes: Optional[bool],
         exclude: Tuple[str, ...]):
    """Upgrade projects created from a Cookiecutter template"""
    context = _load_context(context_file)
    if zip_file is not None and _is_valid_file(zip_file):
        click.echo(f"Using zip-file: {zip_file} for upgrade.")
        context['_template'] = zip_file
    project_directory = os.getcwd()
    update_project_template_branch(context,
                                   project_directory,
                                   branch,
                                   upgrade_branch,
                                   merge_now,
                                   push_template_branch_changes,
                                   exclude,
                                   interactive)


def _load_context(context_file: str):
    try:
        context_str = Path(context_file).read_text(encoding="utf-8")
    except FileNotFoundError:
        click.echo(f"Context file not found at: {context_file}\n"
                   f"Make sure you are in the right directory")
        exit(1)
    context = json.loads(context_str)
    return context


def _is_valid_file(zip_file: str):
    # we check only for local files for valid, for remote URLs, cookiecutter can do the test if its valid.
    zip_path = Path(zip_file)
    try:
        if zip_path.exists():
            ZipFile(Path(zip_file)).testzip()
    except BadZipFile:
        click.echo(f"Bad Zip file at: {zip_file}\n"
                   f"Make sure your zip file is correct.")
        exit(1)
    return True
