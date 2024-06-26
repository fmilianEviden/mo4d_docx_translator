import multiprocessing

from ttkthemes.themed_tk import ThemedTk

from UI.Gui import GUI
from services.GenerateDocx import GenerateDocx


def main():
    multiprocessing.freeze_support()
    root = ThemedTk(theme="arc")
    # root.geometry("240x150")
    root.title("Generate Word documentation from MO4D")
    generate_docx = GenerateDocx()
    gui = GUI(root, generate_docx)

    gui.start()


if __name__ == "__main__":
    main()
