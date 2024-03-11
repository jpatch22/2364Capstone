import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from app import Annotation
from tkinter import ttk
from app.models.test_model import Test_Model

class ImageViewer:
    MODELS_AVAILABLE = {"None Selected" : None,
                        "Testing" : Test_Model()
                        }

    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Image Viewer")

        self.width = width
        self.height = height

        self.image_label = tk.Canvas(self.root, width=width, height=height, borderwidth=2, relief="solid")
        self.image_label.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="Cursor Position: (x, y)")
        self.status_label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.image = None
        self.root.bind('<Motion>', self.update_cursor_position)
        self.annotations = []

        labels = list(self.MODELS_AVAILABLE.keys())

        self.label_combobox = ttk.Combobox(self.root, values=labels)
        self.label_combobox.pack(side=tk.RIGHT, padx=10)
        self.label_combobox.set(labels[0])

    def add_annotations(self, annotations):
        """
        Adds boxes in the format [[x1, y1, x2, y2]]
        """
        self.annotations = annotations 

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((self.width, self.height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(self.image)

            # Clear previous drawings on the canvas
            self.image_label.delete("all")

            # Display the image on the canvas
            self.image_label.create_image(0, 0, anchor=tk.NW, image=photo)
            self.image_label.image = photo

            selected_model = self.MODELS_AVAILABLE[self.label_combobox.get()]
            if selected_model:
                self.annotations = selected_model.supply_annotations(self.image)
            else:
                self.annotations = []

    def update_cursor_position(self, event):
        self.image_label.delete('box')
        if self.image:
            x, y = event.x, event.y
    
            # Get the position of the Canvas within its parent
            canvas_x = self.image_label.winfo_x()
            canvas_y = self.image_label.winfo_y()
    
            # Get the size of the canvas
            canvas_width = self.image_label.winfo_width()
            canvas_height = self.image_label.winfo_height()
    
            # Check if the cursor is within the canvas bounds
            if canvas_x <= x < canvas_x + canvas_width and canvas_y <= y < canvas_y + canvas_height:
                # Calculate the relative position within the image
                x_within_image = int((x - canvas_x) / canvas_width * self.image.width)
                y_within_image = int((y - canvas_y) / canvas_height * self.image.height)
    
                # Update the status label with the cursor position relative to the top-left of the image
                # Debugging moment
                # label_str = f"Cursor Position: ({x_within_image}, {y_within_image}) within Image"
                label_str = ""

                for annotation in self.annotations:
                    x1, y1, x2, y2 = annotation.box
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        self.image_label.create_rectangle(x1, y1, x2, y2, outline='red', width=5, tag='box')
                        label_str = annotation.label + " " + label_str
                self.status_label.config(text=label_str)
            else:
                # Cursor is outside the canvas
                self.status_label.config(text="Cursor outside canvas")
    
    def canvas_coords_to_image(self, x, y):
        canvas_x = self.image_label.winfo_x()
        canvas_y = self.image_label.winfo_y()
    
        canvas_width = self.image_label.winfo_width()
        canvas_height = self.image_label.winfo_height()
        if self.image:
            x_within_image = int((x - canvas_x) / canvas_width * self.image.width)
            y_within_image = int((y - canvas_y) / canvas_height * self.image.height)

            return (x_within_image, y_within_image)
        else:
            return None
    

    def image_coords_to_canvas(self, im_x, im_y):
        canvas_x = self.image_label.winfo_x()
        canvas_y = self.image_label.winfo_y()
    
        canvas_width = self.image_label.winfo_width()
        canvas_height = self.image_label.winfo_height()
        if self.image:
            x_canvas = int(im_x * canvas_width / self.image.width) + canvas_x
            y_canvas = int(im_y * canvas_height / self.image.height) + canvas_y 

            return (x_canvas, y_canvas)
        else:
            return None
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root, 400, 300)
    root.mainloop()

