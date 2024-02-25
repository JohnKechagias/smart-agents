import tkinter as tk
from tkinter import filedialog


class ConfigMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Import Configuration")
        self._config_path = "custom.toml"

        button = tk.Button(
            self.window,
            text="Import Configuration!",
            command=self.button_click,
        )
        button.pack(pady=10, padx=20)

    @property
    def config_path(self):
        return self._config_path

    def show(self):
        self.window.mainloop()

    def get_config_file(self) -> str:
        file_path = filedialog.askopenfilename(filetypes=[("TOML files", "*.toml")])
        print(f"Selected file: {file_path}")
        return file_path

    def button_click(self):
        print("Button clicked!")
        if config_path := self.get_config_file():
            self._config_path = config_path
            self.window.destroy()
