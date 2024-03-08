import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="Cursor Position: (x, y)")
        self.status_label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.image = None
        self.boxes = [(0, 0, 100, 100), (150, 50, 250, 150)]
        self.root.bind('<Motion>', self.update_cursor_position)

    def load_image(self):
        #file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(self.image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            self.canvas.config(width=self.image.width, height=self.image.height)
            self.draw_boxes()

    def draw_boxes(self):
        # Draw all predefined boxes on the image
        for box in self.boxes:
            x1, y1, x2, y2 = box
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2)

    def update_cursor_position(self, event):
        if self.image:
            x_within_widget, y_within_widget = event.x, event.y

            # Get the size of the label (widget) displaying the image
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()

            # Calculate the relative position within the image
            x_within_image = int(x_within_widget / label_width * self.image.width)
            y_within_image = int(y_within_widget / label_height * self.image.height)
            # Update the status label with the cursor position relative to the top-left of the image
            self.status_label.config(text=f"Cursor Position: ({x_within_image}, {y_within_image}) within Image")

            # Remove existing boxes
            self.canvas.delete("all")

            # Draw boxes only when the mouse is over the predefined areas
            for box in self.boxes:
                x1, y1, x2, y2 = box
                if x1 <= x_within_image <= x2 and y1 <= y_within_image <= y2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2)



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()

