import logging
from typing import Optional, List
from curvenote.latex import utils
from ..client import Session
from ..models import BlockFormat, BlockKind
from . import utils

logger = logging.getLogger()


class LatexArticle:
    """
    Class to represent an article in the latex project.
    With the abilty to fetch, localize its assets and write itself to file.
    """

    def __init__(self, session: Session, project_id: str, article_id: str):
        self.session = session
        self.project_id = project_id
        self.article_id = article_id
        self.block = None
        self.version = None
        self.children = None
        self.content = ""
        # TODO obvious one to centralise in project or someway
        self.users = []

    @property
    def title(self):
        if self.block:
            return self.block.title
        return ""

    @property
    def description(self):
        if self.block:
            return self.block.description
        return None

    @property
    def authors(self):
        if self.block:
            return self.block.authors
        return []

    @property
    def author_names(self):
        return [
            user.display_name
            for author in self.authors
            for user in self.users
            if user.id == author.user
        ]

    @property
    def date(self):
        if self.version:
            return self.version.date or self.version.date_created
        return None

    def fetch(self, version: Optional[int] = None):
        """Download article and all children in Latex format

        Raises ValueError if download fails.
        """
        block = self.session.get_block(
            self.project_id, self.article_id, kind=BlockKind.article
        )
        version_to_fetch = version or block.latest_version
        children = self.session.get_version_with_children(
            block, version_to_fetch, fmt=BlockFormat.tex
        )
        if len(children.errors) > 0:
            log("There were errors fetching some children")
            for error in children.errors:
                log(error)

        if children.versions.items[0].kind != BlockKind.article:
            raise ValueError("Expected first child to be an article")
        self.block = children.blocks.items[0]
        self.version, *self.children = children.versions.items
        logger.info(
            f"Processing Article: {self.version.id.project}/"
            f"{self.version.id.block}/versions/{self.version.id.version}"
        )

    def localize(
        self,
        session: Session,
        assets_folder: str,
        reference_list: List[utils.LocalReferenceItem],
    ):
        """Parse article content and pull assets to local storage

        - images
        - authors
        - citations

        TODO: this is turning into a double dispatchy thing, maybe article just holds a
        reference to the project
        """
        self._localize_authors(session)
        self._localize_content(session, assets_folder, reference_list)

    def write(self, filepath: str):
        with open(filepath, "w+") as file:
            file.write(self.content)

    def _localize_authors(self, session: Session):
        for author in self.authors:
            try:
                self.users.append(session.get_user(author.user))
            except ValueError as err:
                logger.info(f"Could note get user {author.user}: {err}")
                continue

    def _localize_content(
        self, session: Session, assets_folder: str, reference_list: List[str]
    ):
        """
        Ignores blocks of any type other than Content and Output.
        """
        concatenated_content = ""
        for child in self.children:
            if child.kind == BlockKind.content:
                logger.info("Content Block")
                content = utils.localize_images_from_content_block(
                    self.session, assets_folder, child.content
                )
                content = utils.localize_references_from_content_block(
                    session, reference_list, content
                )
            elif child.kind == BlockKind.output:
                logger.info(f"Output Block - num outputs: {len(child.outputs)}")
                content = utils.localize_images_from_output_block(assets_folder, child)
            else:
                logger.warning(f"Can't process block with kind:{child.kind} yet")
                continue

            concatenated_content += content + "\n"

        self.content = concatenated_content
