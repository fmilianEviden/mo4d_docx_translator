import os
import json
import time
import re

from services.Translate import Translate
from bs4 import BeautifulSoup, Tag
from docx import Document

from utils.BuildResolve import resolve_route
from utils.WordManipulation import get_image, get_table, add_element_to_word

mapping_tags = {
    'img': lambda t: get_image,
    'table': lambda t: get_table,
}


class GenerateDocx:
    def __init__(self):
        self.route = None
        self.language: str = "English"
        self.api_key = None

        self.word_file = './output/document'  # Provisional
        self.doc = None
        self.doc_json = {}
        self.styles = self.get_styles()
        self.output = None
        self.external_template = None

    @staticmethod
    def get_styles() -> dict:
        """Define Word template styles"""
        try:
            with open(resolve_route('./assets/styles.json'), "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError("Failed to load styles. File not found.")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error parsing JSON: {e}") from e

    def html_to_word(self, directory_path, idx: int):
        html_file = None
        if not os.path.isdir(directory_path):
            return []
        for filename in os.listdir(directory_path):
            if filename.endswith(".html"):
                html_file = os.path.join(directory_path, filename)
                break

        # Get the file name without the extension
        file_name = os.path.splitext(os.path.basename(html_file))[0]

        page = []
        tag_list = list(self.styles.keys())
        tag_list.count('img') < 1 and tag_list.append('img')
        tag_list.count('table') < 1 and tag_list.append('table')
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as file:
            soup = BeautifulSoup(file, 'html.parser')

        for tag in soup.find_all(tag_list):
            if mapping_tags.get(tag.name):
                page.append(
                    mapping_tags[tag.name](tag)(tag, html_file)
                )
            elif tag.name == 'p':
                for content in tag.contents:
                    if isinstance(content, str):
                        match = re.search(r'\*\*(.*?)\*\*', content)
                        if match:
                            page.append((match.group(1), 'h3'))
                        else:
                            page.append((content, tag.name))
                    elif isinstance(content, Tag) and content.name == 'br':
                        page.append(("", "p"))
            else:
                page.append((tag.get_text(), tag.name))
        return page

    def generate(self, queue):
        self.word_file = f"{self.route}/document" if self.route else self.word_file
        self.doc = Document(resolve_route('./assets/template.docx')) \
            if self.external_template is None \
            else Document(self.external_template)
        print(f"Using template: {self.external_template}" if self.external_template else "Using default template")
        queue.put("true¶Generating documentation...")

        if self.api_key:
            print(f'Using API key: {self.api_key}')

        files = os.listdir(self.route)
        total_files = len(files)

        translate = Translate(self.language, self.api_key, queue, self.styles)

        for i, md in enumerate(files, start=1):
            path = os.path.join(self.route, md)
            queue.put(f"true¶Generating documentation for {md.split("-")[0]}...¶{i}/{total_files}")
            page = self.html_to_word(path, idx=i)
            if not page:
                continue
            # Translate
            if self.language != 'English':
                queue.put(f"true¶Translating {md.split("-")[0]}...¶{i}/{total_files}")
                self.doc = translate.generate_from_english(self.doc, page, md.split("-")[0])
            else:
                try:
                    for p in page:
                        self.doc = add_element_to_word(content=p[0], style=p[1], doc=self.doc, styles_dict=self.styles)
                except Exception as e:
                    print(f"Error adding content to document: {e}")

        self.doc.save(f"{self.word_file}_{self.language.lower()}.docx")

        queue.put("true¶Documentation generated successfully.")
        time.sleep(1)
        queue.put("false¶Documentation generated successfully.")
