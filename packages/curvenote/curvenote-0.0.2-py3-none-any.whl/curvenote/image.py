from tempfile import NamedTemporaryFile
from typing import Optional

import requests

from .models import BlockKind, BlockPost, BlockVersion, ImageVersionPost, Project
from .utils import github_to_raw, is_url

IMAGE_TAG = (
    '<img src="{src}" alt="{alt}" title="{title}" align="{align}" width="{width}%">'
)
BLOCK_SRC = "block:{project}/{block}/{version}"


class Image:
    def __init__(self, filename: str, session, content_type: Optional[str] = None):
        self.session = session
        if content_type:
            self.content_type = content_type
        elif filename.lower().endswith("png"):
            self.content_type = "image/png"
        elif filename.lower().endswith("gif"):
            self.content_type = "image/gif"
        elif filename.lower().endswith("jpg") or filename.lower().endswith("jpeg"):
            self.content_type = "image/jpg"
        else:
            raise ValueError(f"unsupported image type: {filename}")
        self.filename = filename

    def upload(self, project: Project, title: Optional[str] = None) -> BlockVersion:
        """Upload an image to given project

        If the image file is a URL, the image will be downloaded and copied
        to user uploads in curvenote.

        Raises ``ValueError`` if upload fails.
        """
        if is_url(self.filename):
            self.filename = github_to_raw(self.filename)
            resp = requests.get(self.filename)
            if resp.status_code >= 400:
                raise ValueError(f"Unable to find image {self.filename}")
            with NamedTemporaryFile() as file:
                file.write(resp.content)
                path = self.session.upload_file(file.name, self.content_type)
        else:
            path = self.session.upload_file(self.filename, self.content_type)
        block = self.session.upload_block(
            BlockPost(kind=BlockKind.image, tags=[]), project
        )
        version = self.session.upload_version(
            ImageVersionPost(upload_path=path, title=title), block
        )
        return version

    def create_tag(
        self,
        project: Project,
        title: Optional[str] = None,
        alt: Optional[str] = None,
        align: str = "center",
        width: int = 70,
    ) -> str:
        version = self.upload(project, title or alt)
        src = BLOCK_SRC.format(**version.id.dict())
        return IMAGE_TAG.format(
            title=title or "", alt=alt or "", src=src, align=align, width=width
        )
