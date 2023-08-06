from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import AnyHttpUrl, BaseModel
from pydantic.generics import GenericModel


class SelfLinks(BaseModel):
    self: AnyHttpUrl


class ListLinks(SelfLinks):
    next: Optional[AnyHttpUrl]


class UserLinks(SelfLinks):
    photo: AnyHttpUrl


class MyUserLinks(UserLinks):
    projects: AnyHttpUrl
    banner: AnyHttpUrl
    access: AnyHttpUrl


class User(BaseModel):
    id: str
    username: str
    display_name: str
    bio: str
    location: str
    website: str
    github: str
    twitter: str
    affiliation: str
    orcid: str
    date_created: datetime
    links: UserLinks


class MyUser(User):
    email: str
    email_verified: bool
    links: MyUserLinks


class ProjectLinks(SelfLinks):
    access: AnyHttpUrl
    team: AnyHttpUrl
    blocks: AnyHttpUrl
    manifest: AnyHttpUrl


class ProjectVisibility(str, Enum):
    """"""

    public = "public"
    private = "private"
    manifest = "manifest"


class ProjectPost(BaseModel):
    team: str
    name: str
    title: Optional[str]
    description: Optional[str]


class Project(ProjectPost):
    id: str
    created_by: str
    visibility: ProjectVisibility
    date_created: datetime
    date_modified: datetime
    links: ProjectLinks


class ProjectList(BaseModel):
    items: List[Project]
    links: ListLinks


class Author(BaseModel):
    plain: Union[str, None]
    user: Union[str, None]


class BlockKind(str, Enum):
    """"""

    article = "Article"
    code = "Code"
    content = "Content"
    image = "Image"
    navigation = "Navigation"
    notebook = "Notebook"
    output = "Output"
    quote = "Quote"
    reference = "Reference"


class BlockID(BaseModel):
    project: str
    block: str


class BlockLinks(SelfLinks):
    project: AnyHttpUrl
    comments: Optional[AnyHttpUrl]
    versions: AnyHttpUrl
    created_by: AnyHttpUrl
    drafts: Optional[AnyHttpUrl]
    default_draft: Optional[AnyHttpUrl]
    latest: Optional[AnyHttpUrl]
    published: Optional[AnyHttpUrl]


class BlockPost(BaseModel):
    kind: BlockKind
    name: Optional[str]
    tags: Optional[List[str]]


class Block(BlockPost):
    id: BlockID
    title: str
    description: str
    latest_version: Optional[int]
    published: bool
    published_versions: Optional[List[int]]
    default_draft: Optional[str]
    num_versions: Optional[int]
    num_comments: Optional[int]
    created_by: str
    date_created: datetime
    date_modified: Optional[datetime]
    authors: Optional[List[Author]]
    links: BlockLinks


class BlockList(BaseModel):
    items: List[Block]
    links: ListLinks


class CommentID(BaseModel):
    project: str
    block: str
    comment: str


class CommentLinks(SelfLinks):
    block: AnyHttpUrl


class Comment(BaseModel):
    id: CommentID
    content: str
    created_by: str
    parent: Optional[str]
    children: List[str]
    date_created: datetime
    date_modified: datetime
    links: CommentLinks


class CommentList(BaseModel):
    items: List[Comment]
    links: ListLinks


class BlockChildID(BaseModel):
    project: str
    block: str
    version: Optional[int]
    draft: Optional[str]


class BlockFormat(str, Enum):
    """"""

    html = "html"
    md = "md"
    jupyter = "jupyter"
    tex = "tex"
    json = "json"
    bibtex = "bibtex"


class BlockChild(BaseModel):
    id: str
    src: BlockChildID


class BlockVersionLinks(SelfLinks):
    download: Optional[AnyHttpUrl]
    project: AnyHttpUrl
    block: Optional[AnyHttpUrl]
    versions: AnyHttpUrl
    drafts: Optional[AnyHttpUrl]
    created_by: AnyHttpUrl
    parent: Optional[AnyHttpUrl]


class ContentVersionPost(BaseModel):
    content: str
    format: Optional[BlockFormat]


class ArticleVersionPost(BaseModel):
    order: List[str]
    children: Dict[str, BlockChild]
    title: Optional[str]


class ImageVersionPost(BaseModel):
    upload_path: AnyHttpUrl


class NavigationItem(BaseModel):
    id: str
    parentId: Optional[str] = None
    title: str
    blockId: BlockID


class NavigationVersionPost(BaseModel):
    items: List[NavigationItem]


class Target(str, Enum):
    """"""

    JupyterMarkdown = "jupyter.markdown"
    JupyterRaw = "jupyter.raw"
    JupyterCode = "jupyter.code"
    JupyterOutput = "jupyter.output"


class OutputSummaryKind(str, Enum):
    """"""

    stream = "stream"
    text = "text"
    error = "error"
    image = "image"
    svg = "svg"
    html = "html"
    latex = "latex"
    json = "json"
    javascript = "javascript"
    plotly = "plotly"
    bokeh = "bokeh"
    ipywidgets = "ipywidgets"
    unknown = "unknown"


class CellOutputMimeTypes(str, Enum):
    """"""

    TextPlain = "text/plain"
    TextHtml = "text/html"
    TextLatex = "text/latex"
    ImagePng = "image/png"
    ImageBmp = "image/bmp"
    ImageJpeg = "image/jpeg"
    ImageSvg = "image/svg+xml"
    ImageGif = "image/gif"
    AppJson = "application/json"
    AppGeoJson = "application/geo+json"
    AppPlotly = "application/vnd.plotly.v1+json"
    AppVega = "application/vnd.vega.v5+json"
    AppVegaLite = "application/vnd.vegalite.v3+json"
    AppVirtualDom = "application/vdom.v1+json"
    AppJavascript = "application/javascript"
    AppWidgetView = "application/vnd.jupyter.widget-view+json"
    AppWidgetState = "application/vnd.jupyter.widget-state+json"
    AppBokehLoad = "application/vnd.bokehjs_load.v0+json"
    AppBokehExec = "application/vnd.bokehjs_exec.v0+json"


class OutputSummaryEntry(BaseModel):
    kind: OutputSummaryKind
    content_type: CellOutputMimeTypes
    content: Optional[str]
    link: Optional[str]


class OutputSummary(OutputSummaryEntry):
    alternate: Dict[OutputSummaryKind, OutputSummaryEntry]


# TODO becoming so optional, losing its usefulness? break out different models per kind?
class BlockVersion(BaseModel):
    id: BlockChildID
    kind: BlockKind
    format: Optional[BlockFormat]
    title: str
    description: str
    published: bool
    created_by: str
    date_created: datetime
    version: int
    parent: Optional[str]
    links: Optional[BlockVersionLinks]

    # Kind: Content
    targets: Optional[List[str]]
    content: Optional[str]  # references return objects
    metadata: Optional[dict]

    # Kind: Image
    size: Optional[int]
    content_type: Optional[str]
    md5: Optional[str]

    # Kind: Article
    date: Optional[datetime]
    order: Optional[List[str]]
    children: Optional[Dict[str, BlockChild]]

    # Kind: Navigation
    items: Optional[List[NavigationItem]]

    # Kind: Output
    targets: Optional[List[Target]]
    outputs: Optional[List[OutputSummary]]
    original: Optional[Any]
    upload_path: Optional[str]
    size: Optional[int]
    content_type: Optional[str]
    md5: Optional[str]


class BlockVersionList(BaseModel):
    items: List[BlockVersion]
    links: ListLinks


class BlockDraftData(BaseModel):
    title: str
    order: List[str]
    children: Dict[str, BlockChild]


class BlockDraftLinks(SelfLinks):
    block: AnyHttpUrl
    child: Optional[AnyHttpUrl]
    parent: Optional[AnyHttpUrl]


class BlockDraft(BaseModel):
    id: BlockChildID
    kind: BlockKind
    data: Union[BlockDraftData, BaseModel]
    parent: Optional[str]
    child: int
    locked: bool
    merged: bool
    merged_by: Optional[str]
    created_by: str
    date_created: datetime
    date_modified: datetime
    links: BlockDraftLinks


class BlockDraftList(BaseModel):
    items: List[BlockDraft]
    links: ListLinks


class AccessID(BaseModel):
    project: str
    user: str


class AccessKind(str, Enum):
    """"""

    user = "user"


class AccessRole(str, Enum):
    """"""

    project_owner = "project.owner"
    project_editor = "project.editor"
    project_comment = "project.comment"
    project_view = "project.view"


class AccessLinks(SelfLinks):
    project: AnyHttpUrl
    user: AnyHttpUrl


class Access(BaseModel):
    id: AccessID
    kind: AccessKind
    role: AccessRole
    date_created: datetime
    date_modified: datetime
    links: AccessLinks


class AccessList(BaseModel):
    items: List[Access]
    links: ListLinks


Item = TypeVar("Item")


class ItemList(GenericModel, Generic[Item]):
    items: List[Item]


class ChildrenList(BaseModel):
    blocks: ItemList[Block]
    versions: ItemList[BlockVersion]
    errors: List
