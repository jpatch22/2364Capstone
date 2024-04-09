from app.models.model import Model
from app.Annotation import Annotation

class Resnet(Model):
    def __init__(self):
        super().__init__()

    def supply_annotations(self, image_list):
        imdic = {}

        for i in range(len(image_list)):
            annotations = []

        return imdic
