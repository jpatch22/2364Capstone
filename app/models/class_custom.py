from app.models.custom_classification.imageClassifier import ImageClassifier
from app.models.model import Model
from app.Annotation import Annotation

class Class_Custom(Model):
    def __init__(self):
        width, height = 224, 224
        num_classes = 10
        self.model = ImageClassifier(height, width, num_classes)
        super().__init__()

    def supply_annotations(self, image_list):
        annotations = []
        for img in image_list:
            label = self.model(self.model.transform(img))
            annotation = Annotation(None, None, None, None, label)
            annotation.box = None
            annotations.append(annotation)

        return annotations
