import time
from tkinter import N, S, E, W, ttk, StringVar, Toplevel
import queue


class LoadingScreen:
    def __init__(self, root, queuee, genereate_button):
        self.root = root
        self.queue = queuee
        self.generate_button = genereate_button
        self.loading_screen = None
        self.progressbar = None

        self.loading_text = StringVar()

        self.check_queue()

    def create_loading_screen(self):
        self.loading_screen = Toplevel(self.root)
        self.loading_screen.protocol("WM_DELETE_WINDOW", self.generate_button.terminate_process)
        self.loading_screen.transient(self.root)
        self.loading_screen.title("Processing...")
        self.loading_screen.resizable(False, False)
        self.loading_screen.grab_set()

        # Set the width and height of the window
        window_width = 240  # Desired width
        window_height = 150  # Desired height
        self.loading_screen.geometry(f"{window_width}x{window_height}")

        position_right = int(self.root.winfo_x() + self.root.winfo_width() / 2 - window_width / 2)
        position_down = int(self.root.winfo_y() + self.root.winfo_height() / 2 - window_height / 2)
        self.loading_screen.geometry("+{}+{}".format(position_right, position_down))

        frame = ttk.Frame(self.loading_screen)
        frame.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W)
        frame.config(width=window_width, height=window_height)
        frame.grid_propagate(False)

        frame_label = ttk.Frame(frame, height=60)
        frame_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        frame_label.grid_propagate(False)

        loading_label = ttk.Label(frame_label, textvariable=self.loading_text, width=100, wraplength=200)
        loading_label.pack()

        self.progressbar = ttk.Progressbar(frame, mode='determinate', maximum=100)
        self.progressbar["value"] = 0
        self.progressbar.grid(row=1, column=0, columnspan=1, padx=(20, 350), pady=10, sticky="ew")

        cancel_button = ttk.Button(frame, text="Cancel", command=self.cancel_and_close)
        cancel_button.grid(row=2, column=0, columnspan=1, padx=(20, 350), pady=10, sticky="ew")

    def check_queue(self):
        try:
            msg = self.queue.get(0)
            if msg.split("¶")[0] == "true":
                if self.loading_screen is None:
                    self.create_loading_screen()
                self.loading_text.set(msg.split("¶")[1])
                if len(msg.split("¶")) == 3:
                    fraction = msg.split("¶")[2]
                    numerator, denominator = map(int, fraction.split('/'))
                    percentage = (numerator / (denominator + 1)) * 100
                    if self.progressbar is not None:
                        self.progressbar["value"] = percentage
            else:
                self.loading_screen.destroy()
                self.loading_screen = None
                self.progressbar.destroy()
                self.progressbar = None

            self.loading_text.set(msg.split("¶")[1])
        except queue.Empty:
            pass

        self.root.after(100, self.check_queue)

    def cancel_and_close(self):
        self.generate_button.terminate_process()
        self.loading_text.set("Cancelled")
        time.sleep(1)
        self.loading_screen.destroy()
        self.loading_screen = None
        self.progressbar.destroy()
        self.progressbar = None
