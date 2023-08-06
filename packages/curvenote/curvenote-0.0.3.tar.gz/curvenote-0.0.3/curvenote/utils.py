import os
import re
from typing import Dict
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from pydantic import AnyHttpUrl


def update_query(
    url: AnyHttpUrl,
    query: Dict[str, str],
) -> AnyHttpUrl:
    """Add query strings to URL"""
    parsed_url = urlparse(url)
    parsed_query = parse_qs(parsed_url.query)
    parsed_query.update(query)
    unparsed_url = urlunparse(
        tuple(parsed_url[:4] + (urlencode(parsed_query, doseq=True),) + parsed_url[5:])
    )
    return unparsed_url


def is_url(value: str) -> bool:
    """Returns True if value is URL"""
    return urlparse(value).scheme and urlparse(value).netloc


def github_to_raw(url: AnyHttpUrl) -> AnyHttpUrl:
    """Converts a github.com URL to raw.githubusercontent.com URL...

    Sketchy.
    """
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")


def title_to_name(title: str) -> str:
    """Replace all non-alphanumeric characters with hyphens"""
    name = re.sub("[^0-9a-z]+", "-", title.lower())[:50]
    while name.startswith("-"):
        name = name[1:]
    while name.endswith("-"):
        name = name[:-1]
    return name


def filename_to_title(filename: str) -> str:
    """Remove path and extension from filename"""
    return filename.split(os.path.sep)[-1].rsplit(".", 1)[0]
