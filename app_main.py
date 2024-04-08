from app.image_viewer import ImageViewer
from app.performance_tests import Performance_Tests
import tkinter as tk
from app.Annotation import Annotation

def main():
    root = tk.Tk()
    #root2 = tk.Tk()
    app = ImageViewer(root, 500, 500)
    #pwindow = Performance_Tests(root2, 500, 500)
    root.mainloop()

if __name__ == "__main__":
    main()
