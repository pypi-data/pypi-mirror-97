import os
import re
import time
import logging
from collections import namedtuple
from typing import List
import requests
from ..client import API_URL, Session
from ..models import Block, BlockVersion, OutputSummaryKind

logger = logging.getLogger()

ImageFormats = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif"}
ImageSummary = namedtuple("ImageSummary", ["content", "block_paths", "local_paths"])

LocalReferenceItem = namedtuple(
    "LocalReferenceItem", ["block_path", "local_tag", "bibtex"]
)

INLINE_IMAGE_BLOCK_REGEX = (
    r".*\\includegraphics.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+)}.*\\*"
)
OUTPUT_IMAGE_BLOCK_REGEX = (
    r".*\\includegraphics.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+"
    r"-output-[0-9]+)}.*\\*"
)
OUTPUT_SVG_BLOCK_REGEX = (
    r".*\\includesvg.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+"
    r"-output-[0-9]+)}.*\\*"
)
INLINE_CITATION_BLOCK_REGEX = r"\\cite[pt]?{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20})}"


def find_groups_in_content(regex_matcher: str, content: str):
    """
    Take a peice of tex content that we expect to contain one or more commands,
    find all instances based on the regex given and return the first groups

    Typically this is used to extract block_paths for different latex commands from
    TeX content
    """
    block_paths = []
    matches = re.finditer(regex_matcher, content)
    for match in matches:
        block_path = match[1]
        block_paths.append(block_path)

    return block_paths


def patch_local_images_from_tex_block(regex_matcher: str, content: str):
    """
    Take a peice of tex content that we expect to contain only one includegraphics directive
    get the remote path, assign a new local path and retrun a strcutre that can be parsed
    """
    updated_content = content
    block_paths = []
    local_paths = []
    matches = re.finditer(regex_matcher, content)
    for match in matches:
        block_path = match[1]
        hash_segment = block_path[6:]
        local_segment = hash_segment.replace("/", "_")
        local_path = block_path.replace("block:", "images/").replace(
            hash_segment, local_segment
        )
        updated_content = updated_content.replace(block_path, local_path)
        block_paths.append(block_path)
        local_paths.append(local_path)

    return ImageSummary(
        content=updated_content,
        block_paths=block_paths,
        local_paths=local_paths,
    )


def block_hash_to_url(block_hash: str):
    match = re.search(
        r"block:([A-Za-z0-9]{20})/([A-Za-z0-9]{20})/*([0-9]*)", block_hash
    )
    if match:
        if match[3]:
            return f"{API_URL}/blocks/{match[1]}/{match[2]}/versions/{match[3]}"
        return f"{API_URL}/blocks/{match[1]}/{match[2]}"
    raise ValueError(f"invalid block hash {block_hash}")


# TODO move to session - easier to mock
def get_model(session, url, model=BlockVersion):
    block = session._get_model(url, model)
    if not block:
        raise ValueError(f"Could not fetch the block {url}")
    return block


def fetch(url: str):
    resp = requests.get(url)
    if resp.status_code >= 400:
        raise ValueError(resp.content)
    return resp.content


def localize_images_from_content_block(
    session: Session, assets_folder: str, content: str
):
    patch = patch_local_images_from_tex_block(INLINE_IMAGE_BLOCK_REGEX, content)
    content_with_extensions = patch.content

    for block_path, local_path in zip(patch.block_paths, patch.local_paths):
        # get block
        url = block_hash_to_url(block_path)
        image_block = session._get_model(url, BlockVersion)
        if not image_block:
            raise ValueError(f"Could not fetch image block {url}")

        # download from links.download (signed) to local path
        if not image_block.links.download:
            raise ValueError(f"Block kind {image_block.kind} has no download link")

        resp = requests.get(image_block.links.download)
        if resp.status_code >= 400:
            raise ValueError(resp.content)

        # now that we have the block we need to update the local path in the content
        # and save the file with the correct file extension
        content_type = resp.headers.get("content-type")
        if content_type not in ImageFormats:
            raise ValueError(f"Unsupported image content type {content_type}")
        ext = ImageFormats[content_type]
        local_path_with_extension = f"{local_path}.{ext}"
        content_with_extensions = content_with_extensions.replace(
            local_path, local_path_with_extension
        )

        logging.info(f"Writing {local_path_with_extension}")
        with open(
            os.path.join(assets_folder, local_path_with_extension), "wb+"
        ) as file:
            file.write(resp.content)

    return content_with_extensions


def localize_images_from_output_block(assets_folder: str, output_version: BlockVersion):
    all_content = ""
    for i, output_summary in enumerate(output_version.outputs):
        if (
            output_summary.kind == OutputSummaryKind.image
            or output_summary.kind == OutputSummaryKind.svg
        ):
            logging.info("Output Summary %s" % output_summary.kind)
            patch = patch_local_images_from_tex_block(
                OUTPUT_IMAGE_BLOCK_REGEX
                if output_summary.kind == OutputSummaryKind.image
                else OUTPUT_SVG_BLOCK_REGEX,
                output_summary.content,
            )
            if patch is not None:
                # TODO won't work for non image outputs or multi outputs with
                # mixed image and non image
                if not output_summary.link:
                    raise ValueError(
                        f"OutputSummary {i} in version "
                        f"{output_version.id.project}/{output_version.id.block}/"
                        f"{output_version.id.version} has no download link"
                    )

                fetched_content = fetch(output_summary.link)

                extension = ImageFormats[output_summary.content_type.lower()]
                local_path_with_extension = f"{patch.local_paths[0]}.{extension}"
                patched_content_with_ext = patch.content.replace(
                    patch.local_paths[0], local_path_with_extension
                )
                all_content = all_content + "\n" + patched_content_with_ext

                logging.info(f"Writing {local_path_with_extension}")
                with open(
                    os.path.join(assets_folder, local_path_with_extension), "wb+"
                ) as file:
                    file.write(fetched_content)

        elif output_summary.kind == OutputSummaryKind.text:
            logging.info(f"Output Summary {output_summary.kind}")
            if output_summary.link:
                # text content can be large and may be stored in a file
                content = fetch(output_summary.link).decode("utf-8")
            else:
                content = output_summary.content
            all_content = all_content + "\n" + content
        else:
            logging.info(f"WARNING: Unknown Output Summary: {output_summary.kind}")
            patch = None

    return all_content


def localize_references_from_content_block(
    session: Session, reference_list: List[LocalReferenceItem], content: str
):
    """Looks for cite TeX commands in the content then replaces the block ids
    with locally unique identifiers based on the local reference list.

    The reference list is extended as new references are found (side effect)

    Appends a unique hash to each new reference encountered
    """
    block_paths = find_groups_in_content(INLINE_CITATION_BLOCK_REGEX, content)
    patched_content = content

    for block_path in block_paths:
        # check for the reference in the reference list based on the block_path
        matched_references = [r for r in reference_list if r.block_path == block_path]
        existing_reference = (
            matched_references[0] if (len(matched_references) > 0) else None
        )

        if existing_reference is None:
            url = block_hash_to_url(block_path)
            block = get_model(session, url, Block)

            # get latest version
            version = get_model(
                session, f"{url}/versions/{block.latest_version}?format=bibtex"
            )

            # update the list
            local_tag, plain_tag = parse_cite_tag_from_version(version.content)
            bibtex = version.content.replace(plain_tag, local_tag)

            reference_item = LocalReferenceItem(block_path, local_tag, bibtex)
            reference_list.append(reference_item)
            existing_reference = reference_item
            logging.info(f"using new reference {existing_reference.local_tag}")
        else:
            logging.info(f"using existing reference {existing_reference.local_tag}")

        # patch the content and move on
        patched_content = patched_content.replace(
            block_path, existing_reference.local_tag
        )

    return patched_content


def parse_cite_tag_from_version(content: str):
    tag = "ref"
    match = re.match("@article{([0-9a-zA-Z_]+),*\n", content)
    if match is not None:
        tag = match[1].replace(",", "")
    # adding quasi-random hash to save de-duping work
    hash_id = hex(int(time.time()))[2:]
    tag_with_hash = f"{tag}_{hash_id}"

    return tag_with_hash, tag
