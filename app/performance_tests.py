import tkinter as tk


class Performance_Tests:
    def __init__(self, root, width, height):
        self.root = root
        title = "Performance Testing"
        self.root.title(title)
        self.width = width
        self.height = height
        button = tk.Button(root, text="Click me!", command=self.button_callback)
        button.pack()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

    def button_callback(self):
        pass

    def set_image(self):
        pass

    def run_test(self):
        pass

