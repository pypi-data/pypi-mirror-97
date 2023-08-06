import os
from typing import Optional

from .models import Block, BlockFormat, Project
from .utils import filename_to_title, title_to_name

PROCESS_NOTEBOOK_URL = "{api_url}/process/notebook"
NOTEBOOK_CONTENT_TYPE = "application/x-ipynb+json"


class Notebook:

    block_format = BlockFormat.jupyter

    def __init__(self, filename: str, session):
        self.session = session
        self.filename = os.path.abspath(filename)

    def upload(self, project: Project, title: Optional[str] = None) -> Block:
        """Upload Jupyter Notebook to curvenote Project

        If ``title`` is not provided, title will be determined from the notebook
        filename.

        Currently this does not support versioning notebook cells or entire
        notebooks; it only uplaods a fresh copy of the notebook.
        """
        if title is None:
            title = filename_to_title(self.filename)
        storage_url = self.session.upload_file(self.filename, NOTEBOOK_CONTENT_TYPE)
        resp = self.session._post(
            PROCESS_NOTEBOOK_URL.format(api_url=self.session.api_url),
            json_dict={
                "project": project.id,
                "name": title_to_name(title),
                "title": title,
                "format": self.block_format,
                "upload_path": storage_url,
            },
        )
        return Block(**resp.json())
