class Annotation:
    def __init__(self, x1, y1, x2, y2, label):
        self.box = [x1, y1, x2, y2]
        self.label = label
