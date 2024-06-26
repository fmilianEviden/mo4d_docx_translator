import multiprocessing
from tkinter import ttk

from UI.StyleInputs import StyleInputs
from services.GenerateDocx import GenerateDocx


class GenerateButton:
    def __init__(self, root, inputs, styles_inputs: StyleInputs, generate_docx_service, queue):
        self.root = root
        self.inputs = inputs
        self.styles_inputs = styles_inputs
        self.generate_docx_service = generate_docx_service
        self.queue = queue
        self.process = None
        self.row = 4

        self.generate_button = self.create_generate_button("disabled")

        self.inputs.language.trace("w", self.update_generate_button_state)
        self.inputs.route.trace("w", self.update_generate_button_state)

    def create_generate_button(self, state):
        frame = ttk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=2,  sticky="ew")

        generate_button = ttk.Button(frame, text="Generate", command=self.generate, state=state)
        generate_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return frame

    def update_generate_button_state(self, *args):
        if self.inputs.language.get() == 'en':
            self.row = 4
        else:
            self.row = 5

        self.generate_button.destroy()
        self.generate_button = None

        state = "disabled" if self.inputs.route.get().startswith("Example:") else "normal"
        self.generate_button = self.create_generate_button(state)

        self.generate_button.grid(row=self.row, column=0, columnspan=2, sticky="ew")

    def generate(self):
        route = self.inputs.route.get()
        language = self.inputs.language.get()
        api_key = self.inputs.api_key.get()

        if self.styles_inputs.styles_dict:
            styles = self.styles_inputs.styles_dict
            self.generate_docx_service.styles = styles

            self.generate_docx_service.external_template = self.styles_inputs.template_file_path.get()

        self.generate_docx_service.route = route
        self.generate_docx_service.language = language
        self.generate_docx_service.api_key = api_key

        output = f"./document_{language.lower()}.docx"
        self.inputs.create_output_textbox(path=output)

        self.process = multiprocessing.Process(target=self.generate_docx_service.generate, args=(self.queue,))
        self.process.start()

    def terminate_process(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
