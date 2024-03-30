import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from app import Annotation
from tkinter import ttk
from app.models.test_model import Test_Model
from app.models.yolov5 import Yolov5 

class ImageViewer:
    MODELS_AVAILABLE = {"None Selected" : None,
                        "Testing" : Test_Model(),
                        "Yolov5" : Yolov5()
                        }
    IMAGE_FILE_TYPES = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]

    def __init__(self, root, width, height):
        print("yolo", self.MODELS_AVAILABLE["Yolov5"])
        self.root = root
        title = "MDA Space Machine Learning Demo"
        self.root.title(title)
        large_font = ("Helvetica", 20)
        label = tk.Label(self.root, text=title, font=large_font)
        #label.grid(row=0,column=0)
        label.pack()

        self.width = width
        self.height = height

        text_label = tk.Label(root, text="Select Model")
        #text_label.grid(row=1, column=1)
        text_label.pack()

        labels = list(self.MODELS_AVAILABLE.keys())
        self.label_combobox = ttk.Combobox(self.root, values=labels)
        #self.label_combobox.grid(row=1,column=2)
        self.label_combobox.pack()
        self.label_combobox.set(labels[0])

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        #self.load_button.grid(row=1, column=0)
        self.load_button.pack()

        self.load_dir_button = tk.Button(self.root, text="Load Image Folder", command=self.load_image_dir)
        self.load_dir_button.pack()

        self.image_label = tk.Canvas(self.root, width=width, height=height, borderwidth=2, relief="solid")
        #self.image_label.grid(row=3, column = 0)
        self.image_label.pack()
        
        self.ann_label = tk.Label(self.root, text="Annotation:")
        self.ann_label.pack(side=tk.LEFT)

        self.status_label = tk.Label(self.root, text="Cursor Position: (x, y)")
        #self.status_label.grid(row=3, column=1)
        self.status_label.pack(side=tk.RIGHT)

        self.image = None # currently showing image
        self.images = []
        self.root.bind('<Motion>', self.update_cursor_position)
        self.annotations = []


    def add_annotations(self, annotations):
        """
        Adds boxes in the format [[x1, y1, x2, y2]]
        """
        self.annotations = annotations 

    def load_image_dir(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            files = self.find_image_files(selected_path)
            self.images = self.load_images(files)
            print(self.images)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=self.IMAGE_FILE_TYPES)

        if file_path:
            self.image = Image.open(file_path)
            self.images = [self.image]
            self.image = self.image.resize((self.width, self.height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(self.image)

            # Clear previous drawings on the canvas
            self.image_label.delete("all")

            # Display the image on the canvas
            self.image_label.create_image(0, 0, anchor=tk.NW, image=photo)
            self.image_label.image = photo

            selected_model = self.MODELS_AVAILABLE[self.label_combobox.get()]
            if selected_model:
                self.annotations = selected_model.supply_annotations([self.image])
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
            if canvas_x <= x < canvas_x + canvas_width and canvas_y <= y < canvas_y + canvas_height and self.annotations:
                # Calculate the relative position within the image
                x_within_image = int((x - canvas_x) / canvas_width * self.image.width)
                y_within_image = int((y - canvas_y) / canvas_height * self.image.height)
    
                # Update the status label with the cursor position relative to the top-left of the image
                # Debugging moment
                # label_str = f"Cursor Position: ({x_within_image}, {y_within_image}) within Image"
                label_str = ""
                index = 0
                for i in range(len(self.images)):
                    if self.images[i] == self.image:
                        index = i
                        break
                print("HERE", index, self.annotations)

                for annotation in self.annotations[index]:
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

    def find_image_files(self, directory):
        image_extensions = tuple([file_type[1][1:] for file_type in self.IMAGE_FILE_TYPES])
        image_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_files.append(os.path.join(root, file))
        return image_files

    def load_images(self, files):
        images = []
        for filename in files:
            img = Image.open(filename)
            images.append(img)
        return images
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root, 400, 300)
    root.mainloop()

