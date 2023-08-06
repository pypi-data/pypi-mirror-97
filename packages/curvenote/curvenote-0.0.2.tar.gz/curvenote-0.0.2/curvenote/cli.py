import os
import sys
import logging
import typer

from .client import Session
from .latex.project import LatexProject

app = typer.Typer()

logger = logging.getLogger()


@app.command()
def push(
    path: str = typer.Argument(..., help="Local file or folder to push to curvenote."),
    project: str = typer.Argument(
        ...,
        help=(
            "Identifier of target Project. PROJECT may match title, name, or id "
            "of an existing Project. If no existing Project is found, a new "
            "Project will be created with title PROJECT."
        ),
    ),
    article: str = typer.Option(
        None,
        help=(
            "Identifier of target Article. ARTICLE may match title, name, or id "
            "of an existing Article. If no existing Article is found, a new "
            "Article will be created with title ARTICLE. ARTICLE is ignored if "
            "PATH is a folder. If PATH is a folder or ARTICLE is not provided, "
            "filename will be used for Article."
        ),
    ),
    team: str = typer.Option(
        None,
        help=(
            "Team to use when creating a new Project. TEAM is ignored if PROJECT "
            "already exists. If PROJECT does not exist and TEAM is not provided, "
            "the new Project will be created under the current user."
        ),
    ),
    token: str = typer.Argument(
        ..., envvar="CURVENOTE_TOKEN", help="API token generated from curvenote.com"
    ),
):
    """Push contents of local file or folder to curvenote Project"""
    if not os.path.exists(path):
        raise ValueError(f"path not found: {path}")
    session = Session(token)
    project_obj = session.get_or_create_project(
        title=project,
        team=team,
    )
    if os.path.isdir(path):
        session.documents_from_folder(folder=path, project=project_obj)
    elif os.path.isfile(path):
        _, file_extension = os.path.splitext(path)
        if file_extension == ".ipynb":
            session.notebook_from_file(
                filename=path, project=project_obj, title=article
            )
        elif file_extension == ".md":
            session.article_from_file(filename=path, project=project_obj, title=article)
        else:
            raise ValueError(f"unsupported file type: {file_extension}")
    else:
        raise ValueError(f"unable to resolve path: {path}")


@app.command()
def pull_as_latex(
    target: str = typer.Argument(
        ...,
        help=(
            "Local folder in which to construct the Latex assets. If TARGET exists it"
            "and all files will be removed and a new empty folder structure created"
        ),
    ),
    project: str = typer.Argument(
        ...,
        help=(
            "Identifier of existing Project containing ARTICLE. PROJECT may match title,"
            " name, or id of an existing Project. If no existing Project is found, an "
            "error will be raised"
        ),
    ),
    article: str = typer.Argument(
        ...,
        help=(
            "Identifier of existing Article. ARTICLE may match title, name, or id "
            "of an existing Article. If no existing Article is found, an error will"
            "be raised."
        ),
    ),
    token: str = typer.Argument(
        ..., envvar="CURVENOTE_TOKEN", help="API token generated from curvenote.com"
    ),
    version: int = typer.Option(
        None,
        help=(
            "Version of the article to pull, if not specified will pull the latest version."
        ),
    ),
):
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    session = Session(token)

    try:
        project = session.get_project(project)
    except ValueError as err:
        typer.echo(f"Could not find project: {project} or you do not have access")
        raise typer.Exit(code=1) from err

    typer.echo(f"Found project: {project.name}")

    document = LatexProject(session, target)

    try:
        # FRANKLIN: Probably a better pattern for logging?
        document.add_article(project, article, version)
    except ValueError as err:
        typer.echo(err)
        raise typer.Exit(code=1)

    document.write()


@app.command()
def get_me(token: str):
    session = Session(token)
    typer.echo(session.user().json(indent=4))


@app.command()
def get_my_projects(token: str):
    session = Session(token)
    for project in session.my_projects():
        typer.echo(project.json(indent=4))
