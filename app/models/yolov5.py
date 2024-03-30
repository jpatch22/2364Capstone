from app.Annotation import Annotation
from app.models.model import Model
import torch

class Yolov5(Model):
    WEIGHTS_PATH = "app/models/planes_premade_3_relu/yolov5s.pt"
    YOLO = "app/models/planes_premade_3_relu/Yolov5"
    def __init__(self):
        super().__init__()
        #self.model = torch.hub.load(self.YOLO, 'custom', path=self.WEIGHTS_PATH, source='local')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.WEIGHTS_PATH, force_reload=True) 


    def supply_annotations(self, image_list):
        imdic = {}
        print("HERE", image_list)
        for i in range(len(image_list)):
            annotations = []
            res = self.model(image_list[i])
            print(res)
            imdic[i] = annotations

        return imdic

    def convert_to_annotations(self, res):
        pass

if __name__ == "__main__":
    model = Yolov5()

