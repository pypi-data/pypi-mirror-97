import os
import logging

from jinja2 import Environment, PackageLoader

from ..client import Session
from .article import LatexArticle


logger = logging.getLogger()


class LatexProject:
    def __init__(self, session: Session, target_folder: str):
        self.session = session
        self.target_folder = os.path.abspath(target_folder)
        self.assets_folder = os.path.join(self.target_folder, "assets")
        self.images_folder = os.path.join(self.target_folder, "assets", "images")
        self.documents_folder = os.path.join(self.target_folder, "documents")
        logger.info(f"Creating {self.images_folder}")
        os.makedirs(self.images_folder, exist_ok=True)
        logger.info(f"Creating {self.documents_folder}")
        os.makedirs(self.documents_folder, exist_ok=True)
        self.articles = []
        self.reference_list = []
        self.jinja = None
        self._configure_jinja()

    def _configure_jinja(self):
        """
        Default jinja syntax doesn't play well with LaTeX.
        Create a custom environment that does.
        http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
        """
        self.jinja = Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=PackageLoader("curvenote", "latex/templates"),
        )

    def add_article(self, project_id: str, article_id: str, version: int):
        latex_article = LatexArticle(self.session, project_id, article_id)
        latex_article.fetch(version)
        latex_article.localize(self.session, self.assets_folder, self.reference_list)

        idx = len(self.articles)
        filename = f"{idx}_{latex_article.block.name}"
        self.articles.append((f"documents/{filename}", latex_article, filename))

    def render(self):
        template = self.jinja.get_template("index.tpl")
        try:
            _, first_article, __ = self.articles[0]
            return template.render(
                article_paths=[p for p, *_ in self.articles],
                main_title=first_article.title,
                main_author_list=first_article.author_names,
                main_day=first_article.date.day,
                main_month=first_article.date.month,
                main_year=first_article.date.year,
            )
        except ValueError as err:
            raise ValueError("Need at least one article") from err

    def write(self):
        for (_, article, filename) in self.articles:
            article_filepath = os.path.join(self.documents_folder, filename + ".tex")
            article.write(article_filepath)

        with open(os.path.join(self.target_folder, "index.tex"), "w+") as file:
            file.write(self.render())

        if len(self.reference_list) > 0:
            with open(os.path.join(self.target_folder, "main.bib"), "w+") as file:
                for reference in self.reference_list:
                    file.write(reference.bibtex)
