import os
import re
from typing import List

from .image import IMAGE_TAG, Image
from .models import (
    ArticleVersionPost,
    Block,
    BlockChild,
    BlockFormat,
    BlockKind,
    BlockPost,
    ContentVersionPost,
    Project,
)
from .utils import github_to_raw, is_url

IMAGE_REGEX = re.compile(r'^!\[(?P<alt>.*)\]\((?P<path>.*?)(\ "(?P<title>.*)")?\)$')


class Markdown:

    block_kind = BlockKind.content
    block_format = BlockFormat.md

    def __init__(self, filename: str, session):
        self.session = session
        self.filename = os.path.abspath(filename)

    def get_sections(self) -> List[str]:
        """Break markdown content into sections to be uploaded as individual blocks

        Image references and code blocks are each given their own section.
        All remaining content is naively split at double line breaks.
        """
        with open(self.filename, "r") as file:
            lines = [line if line.strip() else "" for line in file.read().split("\n")]
        output_sections = []
        section = ""
        tick_code_block = False
        tab_code_block = False
        tex_block = False
        for line in lines:
            if line.strip() == r"\begin{equation}":
                line = "$$"
                tex_block = True
            if line.strip() == r"\end{equation}":
                line = "$$"
                tex_block = False
            if IMAGE_REGEX.match(line):
                if section:
                    output_sections.append(section)
                    section = ""
                output_sections.append(line)
                continue
            if line.startswith("```"):
                tick_code_block = not tick_code_block
            if line.startswith("    ") and not tick_code_block and not tex_block:
                tab_code_block = True
            elif tab_code_block and line:
                tab_code_block = False
                output_sections.append(section.strip("\n"))
                section = ""
            if section and not line and not (tick_code_block or tab_code_block):
                output_sections.append(section)
                section = ""
            elif section:
                section = "\n".join([section, line])
            elif line:
                section = line
        if section:
            output_sections.append(section)
        return output_sections

    def upload(self, article: Block, title: str = None):
        """Upload markdown content to provided article

        Article ``title`` will be set if specified.
        This creates a new version of the article with blocks extracted from the file.
        The extracted blocks are not tied to the blocks in the previous article version.

        Raises ``ValueError`` if upload fails.
        """
        project = self.session.resolve(article.links.project, Project)
        version = ArticleVersionPost(title=title, order=[], children={})
        for i, section in enumerate(self.get_sections()):
            block_format = self.block_format
            image_match = IMAGE_REGEX.match(section)
            if image_match:
                title = image_match.group("title")
                alt = image_match.group("alt")
                path = image_match.group("path")
                if not is_url(path) and not os.path.isabs(path):
                    path = os.path.abspath(
                        os.path.sep.join([os.path.dirname(self.filename), path])
                    )
                try:
                    image = Image(path, self.session)
                except ValueError:
                    if is_url(path):
                        section = IMAGE_TAG.format(
                            title=title or "", alt=alt or "", src=github_to_raw(path)
                        )
                    else:
                        raise
                else:
                    section = image.create_tag(project, title, alt)
                section += "<p></p>"
                block_format = BlockFormat.html
            section_block = self.session.upload_block(
                BlockPost(kind=self.block_kind, tags=[]), project
            )
            section_version = self.session.upload_version(
                ContentVersionPost(content=section, format=block_format),
                section_block,
            )
            local_id = str(i)
            version.children.update(
                {local_id: BlockChild(id=local_id, src=section_version.id)}
            )
            version.order.append(local_id)
        return self.session.upload_version(version, article)
