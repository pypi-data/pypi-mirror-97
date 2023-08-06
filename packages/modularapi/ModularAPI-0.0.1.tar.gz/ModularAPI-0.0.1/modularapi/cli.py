import sys
import os
import venv
import shutil
import subprocess
import time
import json
import re
from pathlib import Path
from importlib import import_module
from contextlib import redirect_stdout

import click
import git

from alembic import command
from alembic.config import Config

from modularapi.settings import get_setting
from modularapi.utils import _on_rmtree_error


class AlembicConfig(Config):
    def get_template_directory(self):
        pkg_dir = Path(__file__).resolve().parent
        return pkg_dir / "templates"


if sys.version_info.major < 3 or sys.version_info.minor < 6:
    click.secho("This framework need Python 3.6 or higher !", fg="red")
    exit(1)

info_style = click.style("INFO", bg="white", fg="black", bold=True)
success_style = click.style("SUCCESS", bg="green", fg="black", bold=True)
warning_style = click.style("WARNING", bg="yellow", fg="black", bold=True)
error_style = click.style("ERROR", bg="red", fg="black", bold=True)


@click.group()
@click.pass_context
def cli(ctx):
    """
    Manage your ModularAPI project with the CLI.
    """
    ctx.ensure_object(dict)
    ctx.obj["start_time"] = time.time()


@cli.resultcallback()
@click.pass_context
def process_result(ctx, result, **kwargs):
    click.echo(f"{success_style} Done in {time.time() - ctx.obj['start_time']:.3f}s.")


# group db
@cli.group(name="db")
def cli_db():
    """
    Manage your PostGreSQL database.
    """


# db branches
@cli_db.command(name="branches")
@click.option("-v", "--verbose", is_flag=True, help="Output in verbose mode.")
def cli_db_branches(verbose):
    """
    Show current branch points.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.branches(config=alembic_cfg, verbose=verbose)


# db current
@cli_db.command(name="current")
@click.option("-v", "--verbose", is_flag=True, help="Output in verbose mode.")
def cli_db_current(verbose):
    """
    Display the current revision for a database.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.current(config=alembic_cfg, verbose=verbose)


# db downgrade <revision>
@cli_db.command(name="downgrade")
@click.argument("revision")
@click.option("--sql", is_flag=True, help="Use the sql mode.")
def cli_db_downgrade(revision, sql):
    """
    Revert to a previous version.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.downgrade(config=alembic_cfg, revision=revision, sql=sql)


# db edit <rev>
@cli_db.command(name="edit")
@click.argument("rev")
def cli_db_edit(rev):
    """
    Edit revision script(s) using $EDITOR.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.edit(config=alembic_cfg, rev=rev)


# db heads
@cli_db.command(name="heads")
@click.option("-v", "--verbose", is_flag=True, help="Output in verbose mode.")
@click.option(
    "--resolve-dependencies",
    is_flag=True,
    help="Treat dependency version as down revisions.",
)
def cli_db_heads(verbose, resolve_dependencies):
    """
    Revert to a previous version.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.heads(
        config=alembic_cfg, verbose=verbose, resolve_dependencies=resolve_dependencies
    )


# db history
@cli_db.command(name="history")
@click.option("--rev-range", default=None, help="String revision range.")
@click.option("-v", "--verbose", is_flag=True, help="Output in verbose mode.")
@click.option("--indicate_current", is_flag=True, help="Indicate current revision.")
def cli_db_history(rev_range, verbose, indicate_current):
    """
    List changeset scripts in chronological order.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.history(
        config=alembic_cfg,
        rev_range=rev_range,
        verbose=verbose,
        indicate_current=indicate_current,
    )


# db merge
@cli_db.command(name="merge")
@click.argument("revisions", nargs=-1)
@click.option(
    "-m", "--message", default=None, help="A string message to apply to the revision"
)
@click.option(
    "--branch-label",
    default=None,
    help="String label name to apply to the new revision",
)
@click.option(
    "--rev-id",
    default=None,
    help="Hardcoded revision identifier instead of generating a new one.",
)
def cli_db_merge(revisions, message, branche_label, rev_id):
    """
    Merge two (or more) revisions together. Creates a new migration file.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.merge(
        config=alembic_cfg,
        revisions=revisions,
        message=message,
        branch_label=branche_label,
        rev_id=rev_id,
    )


# db revision
@cli_db.command(name="revision")
@click.option(
    "--message", "-m", default=None, help="A message to apply to the revision."
)
@click.option(
    "--autogenerate",
    is_flag=True,
    help="Whether or not to autogenerate the script from the database.",
)
@click.option(
    "--sql",
    is_flag=True,
    help="Whether to dump the script out as a SQL string; when specified, the script is dumped to stdout.",
)
@click.option(
    "--head",
    default="head",
    help="Head revision to build the new revision upon as a parent.",
)
@click.option(
    "--splice",
    is_flag=True,
    help="Whether or not the new revision should be made into a new head of its own; is required when the given head is"
    " not itself a head.",
)
@click.option(
    "--branch-label", default=None, help="String label to apply to the branch."
)
@click.option(
    "--version-path",
    default=None,
    help="String symbol identifying a specific version path from the configuration.",
)
@click.option(
    "--rev-id",
    default=None,
    help="Optional revision identifier to use instead of having one generated.",
)
def cli_db_revision(
    message, autogenerate, sql, head, splice, branch_label, version_path, rev_id
):
    """
    Create a new revision file.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", get_setting().PG_DNS)
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.revision(
        config=alembic_cfg,
        message=message,
        autogenerate=autogenerate,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
    )


# db show <rev>
@cli_db.command(name="show")
@click.argument("revisions", required=True)
def cli_db_show(revisions):
    """
    Show the revision(s) denoted by the given symbol.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.show(
        config=alembic_cfg,
        rev=revisions,
    )


# db stamp <revision='head'>
@cli_db.command(name="stamp")
@click.argument("revision", default="head")
@click.option(
    "--sql",
    is_flag=True,
    help="Use the SQL mode.",
)
@click.option(
    "--purge",
    is_flag=True,
    help="Delete all entries in the version table before stamping.",
)
def cli_db_stamp(revision, sql, purge):
    """
    Stamp the revision table with the given revision; don’t run any migrations.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.stamp(config=alembic_cfg, revision=revision, sql=sql, purge=purge)


# db upgrade <revision>
@cli_db.command(name="upgrade")
@click.argument("revision")
@click.option(
    "--sql",
    is_flag=True,
    help="Use the SQL mode.",
)
def cli_db_upgrade(revision, sql):
    """
    Upgrade to a later version.
    """
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("script_location", str(Path() / "db_migrations"))
    command.upgrade(config=alembic_cfg, revision=revision, sql=sql)


# group modules
@cli.group(name="modules")
def cli_modules():
    """
    Manage your modules.
    """


# modules add <git_remote_link>
@cli_modules.command(name="add")
@click.argument("github_repo", type=click.STRING)
def cli_modules_add(github_repo):
    """
    Add a module from a git remote url ( github / gitlab / ect... ).
    """
    p = Path("./modules")

    if not p.is_dir():
        click.echo(
            f"{warning_style} The `modules` directory doesn't exist, creating one ..."
        )
    p.mkdir(parents=True, exist_ok=True)

    m = re.match(r"https?://(.+\..+)/(?P<owner>.+)/(?P<name>.+)(\.git)?", github_repo)
    if m:
        repo_name = f"{m.group('owner')}-{m.group('name')}"
    else:
        # fallback name
        if github_repo.endswith(".git"):
            repo_name = github_repo.split("/")[-1].split(".")[:-1]
        else:
            repo_name = github_repo.split("/")[-1]

    if (p / repo_name).is_dir():
        click.echo(f"{error_style} The module `{repo_name}` is already installed !")
        exit(1)

    click.echo(f"{info_style} Downloading the module ...")

    try:
        git.Repo.clone_from(url=github_repo, to_path=p / repo_name)
    except git.exc.CommandError:
        click.echo(f"{error_style} Repository `{github_repo}` doesn't exist !")
        exit(1)

    click.echo(f"{success_style} The module has been installed in `{p / repo_name}`.")
    click.echo(f"{info_style} Searching for a `requirements.txt` file ...")
    req_file = p / repo_name / "requirements.txt"
    if req_file.is_file():
        click.echo(
            f"{info_style} requirements file found, installing it on the venv ..."
        )

        # on Windows
        if os.name == "nt":
            python_path = Path("venv") / "Scripts" / "python.exe"

        # on Unix
        else:
            python_path = Path("venv") / "bin" / "python"

        subprocess.run(
            [python_path, "-m", "pip", "install", "-r", req_file],
            check=True,
        )
    else:
        click.echo(f"{info_style} requirements files not found.")


# modules remove <module_name>
@cli_modules.group(name="remove", invoke_without_command=True)
@click.argument("module_name")
def cli_modules_remove(module_name):
    """
    Remove a module.
    """

    p = Path("./modules") / Path(module_name)
    if not p.is_dir():
        click.echo(f"{error_style} The module `{module_name}` doesn't exist !")
        exit(1)

    click.echo(f"{info_style} Uninstalling `{module_name}` ...")
    shutil.rmtree(p, onerror=_on_rmtree_error)
    click.echo(f"{success_style} `{module_name}` has been correctly removed.")


# modules remove all
@cli_modules_remove.command(name="all")
def cli_modules_remove_all():
    """
    Remove all modules
    """
    p = Path("./modules")
    if not p.is_dir():
        click.echo(f"{error_style} There is no modules dir !")
        exit(1)

    shutil.rmtree(p, onerror=_on_rmtree_error)
    p.mkdir(parents=True, exist_ok=True)


# modules update <module_name>
@cli_modules.group(name="update", invoke_without_command=True)
@click.argument("module_name")
def cli_modules_update(module_name):
    """
    Update a module from a git remote.
    """
    p = Path("./modules") / module_name

    if not p.is_dir():
        click.echo(f"{error_style} The module `{module_name}` doesn't exist")
        exit(1)

    click.secho(f"{info_style} Updating `{module_name}` ...")

    try:
        repo = git.Repo(p)
    except git.exc.InvalidGitRepositoryError:
        click.echo(
            f"{error_style} the module `{p}` isn't valid (probably missing the .git folder) !",
        )
        exit(1)

    try:
        repo.remotes.origin.pull()
    except git.exc.GitCommandError:
        # In the case the repo was deleted from github/gitlab/ect
        click.echo(f"{error_style} Unable to update, check the remote origin !")
        exit(1)

    click.echo(f"{info_style} `{module_name}` has been updated.")


# modules update all
@cli_modules_update.command(name="all")
def cli_modules_update_all():
    """
    Update all modules.
    """
    p = Path("./modules")
    for module_name in p.glob("*"):
        if module_name.is_dir():
            try:
                repo = git.Repo(p / module_name)
                try:
                    repo.remotes.origin.pull()
                except git.exc.GitCommandError:
                    # In the case the repo was deleted from github/gitlab/ect
                    click.echo(
                        f"{error_style} Unable to update, check the remote origin !"
                    )
            except git.exc.InvalidGitRepositoryError:
                click.echo(
                    f"{warning_style} the module `{module_name}` couldn't be updated !",
                )


# modules build <module_name>
@cli_modules.command(name="build")
@click.argument("module_name")
def cli_modules_build(module_name):
    """
    Build the module.
    """
    p = Path("./modules") / module_name
    if not p.is_dir():
        click.echo(f"{error_style} {module_name} doesn't exists !")
        exit(1)
    try:
        sys.path.append(str(Path().resolve()))
        module = import_module(f"modules.{module_name}.main")
        build_hook = getattr(module, "on_build")
        build_hook()

    except ModuleNotFoundError:
        click.echo(f"{error_style} {module_name} module doesn't have main.py !")
        exit(1)
    except AttributeError:
        click.echo(
            f"{error_style} {module_name} module doesn't have build_module hook !"
        )
        exit(1)
    except TypeError:
        click.echo(f"{error_style} {module_name}.main.build_module is not callable !")
        exit(1)


# modules export <file.json>
@cli_modules.command(name="export")
@click.argument("output_file", type=click.File("w"))
def cli_modules_export(output_file):
    """
    Export all modules as json format.
    """

    repos = {}
    for module_name in Path("./modules").glob("*"):
        if module_name.is_dir():
            try:
                repos[module_name.parts[-1]] = git.Repo(module_name)
            except git.exc.InvalidGitRepositoryError:
                click.echo(
                    f"{warning_style} the module `{module_name}` couldn't be exported !"
                )

    res = {str(path): list(repo.remotes.origin.urls) for path, repo in repos.items()}
    json.dump(res, fp=output_file, indent=4, sort_keys=True)


# modules import <file.json>
@cli_modules.command(name="import")
@click.argument("input_file", type=click.File("r"))
def cli_modules_import(input_file):
    """
    Import all modules from json format file.
    """
    p = Path("./modules")
    for module, repo_urls in json.load(fp=input_file).items():
        try:
            git.Repo.clone_from(url=repo_urls[0], to_path=(p / module))
        except (IndexError, git.exc.GitCommandError):
            click.secho(f"{warning_style} the module `{module}` couldn't be imported !")


# module update list
@cli_modules.command(name="list")
def cli_modules_list():
    """
    List all installed modules.
    """

    p = Path("./modules")

    modules = [m.parts[-1] for m in p.glob("*") if m.is_dir()]
    if modules:
        click.secho("\n".join(f"{m} is installed" for m in modules))
    else:
        click.secho(f"{warning_style} There is no module installed !")


# init <project_name>
@cli.command(name="init")
@click.argument("project_path", type=click.Path())
def cli_projet_init(project_path):
    """
    Init a new Modular project
    """

    p = Path(project_path)

    # check if the path already exists
    if p.is_dir():
        click.secho(f"{error_style} the path `{p}` already exist !")
        exit(1)

    # Initialization
    click.echo(f"{info_style} Initializing a new project at `{p}` ...")
    (p / "modules").mkdir(parents=True)

    alembic_cfg = AlembicConfig(file_=p / "alembic.ini")
    # alembic_cfg.set_main_option("sqlalchemy.url", get_setting().PG_DNS)
    alembic_cfg.set_main_option("script_location", str(p / "db_migrations"))

    # initialize the db migrations
    with open(os.devnull, "w") as f:
        with redirect_stdout(f):
            command.init(
                config=alembic_cfg, directory=p / "db_migrations", template="default"
            )

    # creating the venv
    click.echo(f"{info_style} Creating the venv ...")
    venv.EnvBuilder(with_pip=True).create(p / "venv")

    # install dependancies
    click.echo(f"{info_style} Installing dependancies in the venv ...")

    # on Windows
    if os.name == "nt":
        python_path = p / "venv" / "Scripts" / "python.exe"

    # on Unix
    else:
        python_path = p / "venv" / "bin" / "python"

    subprocess.run([python_path, "-m", "pip", "install", "-U", "pip"], check=True)
    subprocess.run(
        [
            python_path,
            "-m",
            "pip",
            "install",
            "-r",
            Path(__file__).parent / "venv_requirements.txt",
        ],
        check=True,
    )

    shutil.copyfile(
        src=Path(__file__).parent / "venv_requirements.txt",
        dst=p / "requirements.txt",
    )

    with open(p / ".env", "w", encoding="utf-8") as f:
        print('ENVIRONMENT="developpment"', file=f)
        print('PG_DNS="postgres://user:password@host:port/database"', file=f)

    cd_message = click.style(f"cd {p}", bold=True, fg="green")
    modularAPI_message = click.style("ModularAPI", bold=True, fg="green")
    click.echo(
        f"\n{success_style} You can now do `{cd_message}` and start using {modularAPI_message}"
    )
    click.echo(f"\n{warning_style} Don't forget to edit `{p / '.env'}` !")


if __name__ == "__main__":
    cli()
