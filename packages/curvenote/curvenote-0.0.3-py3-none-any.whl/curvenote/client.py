from functools import lru_cache
from glob import glob
from os import environ, path
from typing import Iterator, List, Optional, Type, Union
from urllib.parse import urlparse, urlunparse
import logging
import requests
from pydantic import AnyHttpUrl, BaseModel, ValidationError

from .markdown import Markdown
from .models import (
    Access,
    AccessList,
    ArticleVersionPost,
    Block,
    BlockChild,
    BlockDraft,
    BlockDraftList,
    BlockFormat,
    BlockKind,
    BlockList,
    BlockPost,
    BlockVersion,
    BlockVersionList,
    ChildrenList,
    Comment,
    CommentList,
    ContentVersionPost,
    ImageVersionPost,
    NavigationItem,
    NavigationVersionPost,
    Project,
    ProjectList,
    ProjectPost,
    User,
    MyUser,
)
from .notebook import Notebook
from .utils import filename_to_title, title_to_name, update_query

logger = logging.getLogger()

API_RESPONSE_MODELS = [
    Access,
    AccessList,
    BlockVersion,
    BlockVersionList,
    Block,
    BlockDraft,
    BlockDraftList,
    BlockList,
    Comment,
    CommentList,
    Project,
    ProjectList,
    User,
    MyUser,
]

CLIENT_NAME = "Curvenote Python Client"
CLIENT_VERSION = "0.0.1"
if environ.get("CURVENOTE_ENV") == "development":
    print(
        r"""
  ___            __  __         _
 |   \ _____ __ |  \/  |___  __| |___
 | |) / -_) V / | |\/| / _ \/ _` / -_)
 |___/\___|\_/  |_|  |_\___/\__,_\___|

    """
    )
    API_URL = "http://localhost:8083"
    SITE_URL = "https://localhost:3000"
else:
    API_URL = "https://api.curvenote.com"
    SITE_URL = "https://curvenote.com"
ME_URL = "{api_url}/my/user"
USERS_URL = "{api_url}/users/{user_id}"
PROJECTS_URL = "{api_url}/projects"
UPLOAD_URL = "{api_url}/my/upload"


class Session:
    def __init__(
        self, token: str, api_url: Optional[str] = None, site_url: Optional[str] = None
    ) -> None:
        self.api_url = api_url or API_URL
        self.site_url = site_url or SITE_URL
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "X-Client-Name": CLIENT_NAME,
                "X-Client-Version": CLIENT_VERSION,
            }
        )

    @lru_cache(maxsize=128)
    def _get(self, url: str) -> requests.Response:
        resp = self._session.get(url)
        if resp.status_code >= 400:
            raise ValueError(resp.content)
        return resp

    def _get_model(self, url: str, model: Type[BaseModel]) -> BaseModel:
        resp = self._get(url)
        return model(**resp.json())

    def _get_models(self, url: str, model: Type[BaseModel]) -> Iterator[BaseModel]:
        next_url = url
        while next_url:
            resp = self._get(next_url)
            obj_list = model(**resp.json())
            for obj in obj_list.items:
                yield obj
            next_url = None
            # next_url = obj_list.links.next

    def _post(self, url: str, json_dict: dict) -> requests.Response:
        resp = self._session.post(url, json=json_dict)
        if resp.status_code >= 400:
            raise ValueError(resp.content)
        self._get.cache_clear()
        return resp

    def _delete(self, url: str) -> requests.Response:
        resp = self._session.delete(url)
        if resp.status_code >= 400:
            raise ValueError(resp.content)
        self._get.cache_clear()
        return resp

    def user(self) -> MyUser:
        """User object corresponding to session user

        Raises ``ValueError`` if user cannot be fetched.
        """
        return self.resolve(ME_URL.format(api_url=self.api_url), MyUser)

    def get_user(self, user_id: str) -> User:
        """User object corresponding to the id provided

        Raises ``ValueError`` if user cannot be fetched.
        """
        return self.resolve(
            USERS_URL.format(api_url=self.api_url, user_id=user_id), User
        )

    def my_projects(self, owner: bool = False) -> List[Project]:
        """All projects accessible to the user

        If ``owner = True``, only projects created by the user are returned

        Raises ``ValueError`` if projects cannot be fetched.
        """
        projects = self._get_models(self.user().links.projects, ProjectList)
        if owner:
            return [proj for proj in projects if proj.created_by == self.user().id]
        return list(projects)

    def get_project(self, project: str) -> Project:
        """Retrieve project based on identifier

        First this function tries to match ``project.id``.
        If no match is found, it tries to match ``project.name``.
        Finally, it tries to match ``project.title``.

        Raises ``ValueError`` if the title is non-unique or if no match is found.
        """
        my_projects = self.my_projects()
        for project_obj in my_projects:
            if project_obj.id == project:
                return project_obj
        for project_obj in my_projects:
            if project_obj.name == project:
                return project_obj
        titles = [project_obj.title for project_obj in my_projects]
        if titles.count(project) > 1:
            raise ValueError(f"duplicate projects found: {project}")
        for project_obj in my_projects:
            if project_obj.title == project:
                return project_obj
        raise ValueError(f"unable to find project: {project}")

    def get_block(
        self,
        project: Union[str, Project],
        block: str,
        kind: Optional[BlockKind] = None,
    ) -> Block:
        """Retrieve block based on identifier

        This function will only search within provided ``project``.
        If ``project`` is a string, it will look up with :meth:`get_project`.

        First this function tries to match ``block.id``.
        If no match is found, it tries to match ``block.name``.
        Finally, it tries to match ``block.title``.

        Raises ``ValueError`` if the title is non-unique or if no match is found.
        """
        project_obj = (
            project if isinstance(project, Project) else self.get_project(project)
        )
        possible_blocks = []
        blocks_url = project_obj.links.blocks
        if kind:
            blocks_url = update_query(blocks_url, {"kind": kind})
        for block_obj in self._get_models(blocks_url, BlockList):
            if block_obj.id.block == block:
                return block_obj
            if block in (block_obj.name, block_obj.title):
                possible_blocks.append(block_obj)
        for block_obj in possible_blocks:
            if block_obj.name == block:
                return block_obj
        titles = [block_obj.title for block_obj in possible_blocks]
        if titles.count(block) > 1:
            raise ValueError(f"duplicate blocks found for {block}")
        for block_obj in possible_blocks:
            if block_obj.title == block:
                return block_obj
        raise ValueError(f"unable to find {block}")

    def get_version(self, block: Block, version: int) -> BlockVersion:
        """
        Fetches the a specific version of the Block supplied
        """
        if version > block.latest_version:
            raise ValueError(
                f"trying to fetch version {version} when latest version is {block.latest_version}"
            )
        version_obj = self._get_model(f"{block.links.self}/{version}", BlockVersionList)
        return version_obj

    def get_version_with_children(
        self, block: Block, version: int, fmt: BlockFormat
    ) -> ChildrenList:
        """
        Fetches the children of the Block supplied at the specified version
        """
        if version > block.latest_version:
            raise ValueError(
                f"trying to fetch version {version} when latest version is {block.latest_version}"
            )
        return self._get_model(
            f"{block.links.self}/versions/{version}/children/?format={fmt}",
            ChildrenList,
        )

    def download_version(
        self,
        version: BlockVersion,
        content_format: Optional[BlockFormat] = None,
    ) -> bytes:
        """Download version content in specified format

        Raises ``ValueError`` if version cannot be downloaded.
        """
        url = version.links.download
        if content_format:
            url = update_query(url, query={"format": content_format})
        resp = self._get(url)
        return resp.content

    def resolve(self, url: str, model=None):
        """Resolve URL into :ref:`models-returned-from-the-api`

        All API URLs are valid as well as some URLs from the website.
        If ``model`` is provided, the allowed output will be constrained
        to that type.

        Raises ``ValueError`` if URL cannot be resolved into a known model
        or the provided ``model``.
        """
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
        if base_url not in [self.api_url, self.site_url] or not parsed.path:
            raise ValueError(f"invalid url {url}")
        path_parts = parsed.path.split("/")
        if (
            base_url == self.site_url
            and len(path_parts) > 3
            and path_parts[1].startswith("@")
            and path_parts[3].startswith("!")
        ):
            output = self.get_block(path_parts[2], path_parts[3][1:])
            if model and not isinstance(output, model):
                raise ValueError(f"unable to resolve url {url} to {model.__name__}")
            return output
        if base_url == self.api_url:
            models = [model] if model else API_RESPONSE_MODELS
            resp = self._get(url)
            for mod in models:
                try:
                    return mod(**resp.json())
                except ValidationError:
                    continue
        raise ValueError(
            f"unable to resolve url {url}" + (f" to {model.__name__}" if model else "")
        )

    def upload_file(self, filename: str, content_type: str) -> AnyHttpUrl:
        """Upload file to storage bucket

        Returns reference to the uploaded file.
        Raises ``ValueError`` if upload fails.
        """
        upload_resp = self._post(
            UPLOAD_URL.format(api_url=self.api_url),
            json_dict={"content_type": content_type, "size": path.getsize(filename)},
        )
        storage_url = upload_resp.content.decode("utf-8")
        with open(filename, "rb") as file:
            resp = requests.put(
                storage_url, file.read(), headers={"Content-Type": content_type}
            )
        if resp.status_code >= 400:
            raise ValueError(f"File upload failed: {resp.content}")
        return storage_url

    def upload_block(self, block: BlockPost, project: Project) -> Block:
        """Upload a block to specified project

        Raises ``ValueError`` if upload fails.
        """
        resp = self._post(project.links.blocks, block.dict(exclude_unset=True))
        return Block(**resp.json())

    def upload_version(
        self,
        version: Union[ArticleVersionPost, ContentVersionPost, ImageVersionPost],
        block: Block,
    ) -> BlockVersion:
        """Upload verson of a block

        Currently only Content, Article, and Image blocks are supported.

        Raises ``ValueError`` if upload fails.
        """
        resp = self._post(block.links.versions, version.dict(exclude_unset=True))
        return BlockVersion(**resp.json())

    def article_version_from_file(
        self, filename: str, article: Block, title: Optional[str] = None
    ) -> BlockVersion:
        """Upload new version of local file to curvenote Article

        Article version ``title`` will be set if it is specified.
        Currently only markdown files with ``.md`` extension are supported.

        Raises ``ValueError`` for other file types, if article block is not
        of kind Article, or for failures during upload.
        """
        if article.kind != BlockKind.article:
            raise ValueError(f"block is not an article {article.id.block}")
        if filename.endswith(".md"):
            content = Markdown(filename, self)
        else:
            raise ValueError("only markdown is supported")
        return content.upload(article, title)

    def article_from_file(
        self,
        filename: str,
        project: Project,
        title: Optional[str] = None,
        article_id: Optional[str] = None,
    ) -> BlockVersion:
        """Upload a single file to an Article in a curvenote Project

        First, this tries to find an existing Article, based on ``article_id``,
        which may be the unique Article id or name. If no ``article_id`` is
        provided, it tries to find an existing Article based on ``title`` (or
        ``filename`` if ``title`` is not provided). If no matching Article
        is found, a new Article is created with name based on ``title``
        (or ``filename`` if ``title`` is not provided).

        After finding or creating the Article, a new Version is created
        with the given ``title`` using :meth:`article_version_from_file`.

        Raises ``ValueError`` if there is a problem creating a new Article
        or a new Version of the Article.
        """
        title = title if title is not None else filename_to_title(filename)
        name = title_to_name(title)
        try:
            article_block = self.get_block(
                project, article_id or name, kind=BlockKind.article
            )
        except ValueError:
            article_block = self.upload_block(
                BlockPost(
                    name=name,
                    kind=BlockKind.article,
                    tags=[],
                ),
                project,
            )
        return self.article_version_from_file(filename, article_block, title)

    def notebook_from_file(
        self,
        filename: str,
        project: Project,
        title: Optional[str] = None,
    ) -> BlockVersion:
        """
        Upload a single ipynb notebook to a Curvenote Project

        Note: this currently uses an api endpoint that will not honor existing version information
        the endpoint will only
        """
        title = title if title is not None else filename_to_title(filename)
        notebook = Notebook(filename, self)

        try:
            block = notebook.upload(project, title)
        except ValueError as err:
            raise ValueError("could not upload notebook") from err

        return block

    def documents_from_folder(
        self, folder: str, project: Project, verbose: bool = True
    ) -> Project:
        """Upload contents of a local folder to curvenote Project

        This will attempt to import all .md or .ipynb files from within the folder.
        Calls :meth:`article_from_file` on all .md files
        Calls :meth:`notebook_from_file` on all .ipynb files
        Currently nested folders are not supported.

        Raises ``ValueError`` if there is nothing to upload or upload fails.
        """
        # cannot do multi extension globs so stagger import
        files = sorted(glob(f"{folder}/*.md"))
        if not files:
            if not glob(folder):
                raise ValueError("folder is empty or does not exist")
            logger.info("no markdown (.md) files found")
        else:
            for file in files:
                self.article_from_file(file, project)
                if verbose:
                    logger.info(f"Uploaded...{file[-25:].ljust(25)}", end="\r")

        notebook_files = sorted(glob(f"{folder}/*.ipynb"))
        if not notebook_files:
            if not glob(folder):
                raise ValueError("folder is empty or does not exist")
            logger.info("no notebooks (.ipynb) found")
        else:
            for file in notebook_files:
                self.notebook_from_file(file, project)
                if verbose:
                    logger.info(f"Uploaded...{file[-25:].ljust(25)}")
        if verbose:
            logger.info("\nDone!")
        return project

    def get_or_create_project(
        self,
        title: str,
        team: Optional[str] = None,
    ) -> Project:
        """Get curvenote Project based on title

        First, this tries to find an existing Project, based on ``title``.
        If Project cannot be found, a new Project is created.

        New projects are created under ``team``, if provided;
        otherwise they are created under the current user.
        For existing Projects, ``team`` is ignored.

        Raises ``ValueError`` if Project creation fails.
        """
        name = title_to_name(title)
        try:
            # TODO use /check/project/name service endpoint instead of relying on
            # exception
            project = self.get_project(name)
        except ValueError:
            project_post = ProjectPost(
                team=team if team else self.user().username,
                name=name,
                title=title,
            )
            resp = self._post(
                PROJECTS_URL.format(api_url=self.api_url),
                project_post.dict(exclude_unset=True),
            )
            project = Project(**resp.json())
        return project

    def update_content(
        self,
        project: Project,
        content: str,
        content_format: BlockFormat,
        name: Optional[str] = None,
    ) -> BlockVersion:
        """Upload a new version of a content block

        If ``name`` is provided and a content block of that name is found
        with :meth:`get_block`, a new version of that block will be created.
        Otherwise a new block and new version will be created.
        """
        if name:
            try:
                block = self.get_block(project, name, kind=BlockKind.content)
            except ValueError:
                block = self.upload_block(
                    block=BlockPost(
                        kind=BlockKind.content,
                        name=name,
                    ),
                    project=project,
                )
        else:
            block = self.upload_block(
                block=BlockPost(
                    kind=BlockKind.content,
                ),
                project=project,
            )
        version = self.upload_version(
            version=ContentVersionPost(
                content=content,
                format=content_format,
            ),
            block=block,
        )
        return version

    def update_article(
        self,
        project: Project,
        child_versions: List[BlockVersion],
        title: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> BlockVersion:
        """Upload a new version of an article block

        If an article block of ``title`` or ``name`` is found with
        :meth:`get_block`, a new version of that block will be created.
        Otherwise a new block and new version will be created.
        """
        if not name:
            name = title_to_name(title)
        if not tags:
            tags = []
        try:
            block = self.get_block(project, name, kind=BlockKind.article)
        except ValueError:
            block = self.upload_block(
                block=BlockPost(
                    kind=BlockKind.article,
                    name=name,
                    tags=tags,
                ),
                project=project,
            )
        version = self.upload_version(
            version=ArticleVersionPost(
                order=list(str(i) for i in range(len(child_versions))),
                children={
                    str(i): BlockChild(id=str(i), src=ver.id)
                    for i, ver in enumerate(child_versions)
                },
                title=title,
            ),
            block=block,
        )
        return version

    def update_navigation(
        self, project: Project, articles: List[Block]
    ) -> BlockVersion:
        """Update article order in project navigation

        Add the ``articles`` in the given order to the ``project`` navigation.
        This also deletes the existing draft, so the new version is visible.

        Raises ``ValueError`` if Blocks are invalid or update fails.
        """
        for article in articles:
            if article.kind != BlockKind.article:
                raise ValueError("only article blocks may be added to navigation")
            if article.id.project != project.id:
                raise ValueError(
                    "articles must be part of project to add to navigation"
                )
        nav_blocks = list(
            self._get_models(
                update_query(project.links.blocks, {"kind": "Navigation"}),
                BlockList,
            )
        )
        if len(nav_blocks) != 1:
            raise ValueError(
                f"Unexpected number of navigation blocks in project: {len(nav_blocks)}"
            )
        nav_block = nav_blocks[0]
        nav_version = NavigationVersionPost(
            items=[
                NavigationItem(
                    id=str(i),
                    title=article.title,
                    blockId=article.id,
                )
                for i, article in enumerate(articles)
            ]
        )
        resp = self._post(nav_block.links.versions, json_dict=nav_version.dict())
        if nav_block.links.default_draft:
            self._delete(nav_block.links.default_draft)
        return BlockVersion(**resp.json())
