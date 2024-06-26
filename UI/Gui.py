import multiprocessing
from tkinter import ttk

from UI.GenerateButton import GenerateButton
from UI.Header import Header
from UI.Inputs import Inputs
from UI.LoadingScreen import LoadingScreen
from UI.StyleInputs import StyleInputs


class GUI:
    def __init__(self, root, generate_docx_service):
        self.root = root
        self.header = Header(root)

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Home")

        self.styles_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.styles_tab, text="Styles")

        self.inputs = Inputs(self.home_tab)
        self.styles_inputs = StyleInputs(self.styles_tab)

        self.queue = multiprocessing.Queue()
        self.generate_button = GenerateButton(root, self.inputs, self.styles_inputs, generate_docx_service, self.queue)
        self.loading_screen = LoadingScreen(root, self.queue, self.generate_button)

    def start(self):
        self.root.mainloop()
