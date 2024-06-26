from tkinter import ttk, filedialog, StringVar

from utils.WordManipulation import get_styles_from_user_template


class StyleInputs:
    html_elements = ["p", "h1", "h2", "h3"]

    def __init__(self, root):
        self.root = root

        self.template_file_path = StringVar()
        self.template_file_input = self.create_template_file_input()

        self.styles = []
        self.styles_dict = {}

    def create_template_file_input(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        ttk.Label(frame, text="Template File:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        template_file_input = ttk.Entry(frame, textvariable=self.template_file_path, width=50)
        template_file_input.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        template_file_input.bind("<Button-1>", self.browse_template_file)
        self.template_file_path.set("Example: C:/docs/template.docx")

        return frame

    def browse_template_file(self, event=None):
        template_file_path = filedialog.askopenfilename()
        if not template_file_path or not template_file_path.endswith(".docx"):
            return
        self.template_file_path.set(template_file_path)
        self.styles = get_styles_from_user_template(template_file_path)
        self.create_combo_boxes()

    def create_combo_boxes(self):
        for idx, element in enumerate(self.html_elements):
            row = (idx // 2) + 1
            column = idx % 2

            frame = ttk.Frame(self.root)
            frame.grid(row=row, column=column, sticky="nsew")

            ttk.Label(frame, text=f"{element}:").grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
            style = ttk.Combobox(frame, values=self.styles)
            style.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)

            style.set(self.styles[idx])
            self.styles_dict[element] = style.get()
            style.bind("<<ComboboxSelected>>", self.update_style(element, style))

    def update_style(self, element, style):
        def callback(event):
            self.styles_dict[element] = style.get()
        return callback



