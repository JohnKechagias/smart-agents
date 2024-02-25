import tkinter as tk
from tkinter import filedialog
import shutil
import os

def check_custom_toml_exist():
    return os.path.exists("custom.toml")

class GetConfiguration:
    class Config:
        def __init__(self, file_path):
            self.file_path = file_path

    @classmethod
    def show(cls):
        window = tk.Tk()
        window.title("Import Configuration")

        def get_config_file():
            file_path = filedialog.askopenfilename(filetypes=[("TOML files", "*.toml")])
            print("Selected file:", file_path)
            return file_path

        def copy_to_project_dir(file_path):
            if file_path:
                shutil.copy(file_path, "custom.toml")

        def button_click():
            print("Button clicked!")
            config_path = get_config_file()
            copy_to_project_dir(config_path)
            if config_path:
                window.destroy()
                cls.config = cls.Config(config_path)

        button = tk.Button(window, text="Import Configuration!", command=button_click)
        button.pack(pady=10, padx=20)  

        window.mainloop()

        return "custom.toml" if check_custom_toml_exist() else "config.toml"