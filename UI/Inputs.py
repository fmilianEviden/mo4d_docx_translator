from tkinter import ttk, filedialog, StringVar


class Inputs:
    def __init__(self, root):
        self.root = root

        self.route = StringVar()
        self.docs_root_input = self.create_docs_root_input()

        # self.docs_root_output = self.create_output_textbox()

        self.language = StringVar()
        self.language_radio_buttons = self.create_language_radio_buttons()

        self.api_key = StringVar()
        self.api_key_input = None

        self.language.trace("w", self.update_api_key_input)

    def create_docs_root_input(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        ttk.Label(frame, text="Docs Folder:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        docs_root_input = ttk.Entry(frame, textvariable=self.route)
        docs_root_input.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        docs_root_input.bind("<Button-1>", self.browse_folder)
        self.route.set("Example: C:/workspace/project/docs/v1")

        return frame

    def create_output_textbox(self, path: str):
        frame = ttk.Frame(self.root)
        frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        ttk.Label(frame, text="Docx output:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        docs_root_output = ttk.Label(frame, text=path)
        docs_root_output.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        return frame

    def browse_folder(self, event=None):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        self.route.set(folder_path)

    def create_language_radio_buttons(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

        ttk.Label(frame, text="Language:").grid(row=0, column=0, padx=(20, 32), pady=10, sticky="w")
        self.language.set("English")
        ttk.Radiobutton(frame, text="English", variable=self.language, value="English").grid(row=0, column=1, padx=8,
                                                                                        pady=10, sticky="w")
        ttk.Radiobutton(frame, text="Spanish", variable=self.language, value="Spanish").grid(row=0, column=2, padx=8,
                                                                                        pady=10, sticky="w")
        ttk.Radiobutton(frame, text="French", variable=self.language, value="French").grid(row=0, column=4, padx=8, pady=10,
                                                                                       sticky="w")
        ttk.Radiobutton(frame, text="Portuguese", variable=self.language, value="Portuguese").grid(row=0, column=3, padx=8,
                                                                                           pady=10, sticky="w")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        return frame

    def update_api_key_input(self, *args):
        if self.language.get() != 'English':
            if self.api_key_input is None:
                self.api_key_input = self.create_api_key_input()
        else:
            if self.api_key_input is not None:
                self.api_key_input.destroy()
                self.api_key_input = None

    def create_api_key_input(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

        ttk.Label(frame, text="M04D API Key:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        api_key_entry = ttk.Entry(frame, textvariable=self.api_key)
        api_key_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return frame

