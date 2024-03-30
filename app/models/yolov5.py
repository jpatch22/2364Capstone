from app.Annotation import Annotation
from app.models.model import Model
import torch

class Yolov5(Model):
    WEIGHTS_PATH = "app/models/planes_premade_3_relu/yolov5s.pt"
    YOLO = "app/models/planes_premade_3_relu/Yolov5"
    def __init__(self):
        super().__init__()
        model = torch.hub.load(self.YOLO, 'custom', path=self.WEIGHTS_PATH, source='local') 
#        self.model = torch. 

    def supply_annotations(self, image_list):
        pass

if __name__ == "__main__":
    model = Yolov5()

