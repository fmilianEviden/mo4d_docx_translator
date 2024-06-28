import ast
import json
import time
from queue import Queue

from docx import Document
from itertools import chain
from requests import request, exceptions

from utils.BuildResolve import resolve_route
from utils.WordManipulation import add_element_to_word


class Translate:
    def __init__(self, language: str, api_key: str, queue: Queue, styles_dict: dict):
        self.retries = 15  # Number of retries
        self.wait_time = 1  # Wait time between retries
        self.api_key = api_key
        self.language = language
        self.queue = queue
        self.md = ""
        self.styles_dict = styles_dict
        self.url = "https://machineone4delivery.net/api/v2/mo4d/openai/tools"
        self.files = [('files', ('file', open(resolve_route('./assets/file.txt'), 'rb'), 'application/octet-stream'))]

    def post_request(self, text) -> str:
        prompt = f'Target Language: {self.language}. Translate the first element of each item: {text}'
        msg = ('When generating output, respect the input string format '
               'and the response will be: list[tuple[str, str]]'
               'Also take in mind that the tuple may have a route, '
               'it is very important not to translate the routes'
               'it is very important that the only response output'
               'is the text with format: list[tuple[str, str]]')
        payload = {
            'prompt': prompt,
            'token': self.api_key,
            'language': '',
            'type': 'Language-Translator',
            'temperature': '0.7',
            'message': '[{"role":"system","content":""},{"role":"user","content":"' + msg + '"}]'
        }
        # print(prompt)

        for i in range(self.retries):
            if i != 0:
                self.queue.put(f"true¶Retrying translating {self.md}...")
            try:
                response = request("POST", self.url, headers={}, data=payload, files=self.files)
                print(f'retry_{i}: {response.status_code} --> {response.text}')
                if response.status_code == 200:
                    try:
                        parsed_response = ast.literal_eval(response.json()['response'])
                        return parsed_response
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing JSON response: {e}")
                        # print(f'200_response --> {response.json()['response']}')
                        pass
            except exceptions.RequestException as e:
                print(f"RequestException: {e}")
                pass

            time.sleep(self.wait_time)

        raise Exception("Failed to get a successful response after multiple retries.")

    def generate_from_english(self, doc: Document, page: list, md):
        self.md = md
        text = str(json.dumps(page))
        print(f'Page length --> {len(text)}')

        if len(text) > 5000:
            page = self.split_large_page(page)
            translate = self.split_text(page)
            page = list(chain.from_iterable(page))
        else:
            translate = self.post_request(text=f"""{text}""")

        for i, (page_tuple, translate_tuple) in enumerate(zip(page, translate)):
            if page_tuple[1] == 'img':
                translate[i] = page_tuple

        try:
            for p in translate:
                doc = add_element_to_word(content=p[0], style=p[1], doc=doc, styles_dict=self.styles_dict)
        except Exception as e:
            print(f"Error adding translated content to document: {e}")

        return doc

    def split_text(self, page):

        trim_list = []
        for trim in page:
            text = str(json.dumps(trim))
            trim_list.append(self.post_request(text=f"""{text}"""))
        translate = []
        for t in trim_list:
            translate += t

        return translate

    @staticmethod
    def split_large_page(page, max_length=5000):
        split = []
        current_chunk = []
        current_length = 0

        for item in page:
            current_chunk.append(item)
            current_length += len(str(item))

            if current_length > max_length:
                split.append(current_chunk)
                current_chunk = []
                current_length = 0

        if current_chunk:
            split.append(current_chunk)

        return split
