from app.image_viewer import ImageViewer
import tkinter as tk
from app.Annotation import Annotation

def main():
    root = tk.Tk()
    app = ImageViewer(root, 500, 500)
    annotation1 = Annotation(130, 130, 250, 250, "Supreme Leader")
    app.add_annotations([annotation1])
    root.mainloop()

if __name__ == "__main__":
    main()
