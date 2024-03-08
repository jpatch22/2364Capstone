from app.image_viewer import ImageViewer
import tkinter as tk

def main():
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
