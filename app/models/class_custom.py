from app.models.custom_classification.imageClassifier import ImageClassifier
from app.models.model import Model
from app.Annotation import Annotation
import torch
import yaml
import numpy as np

class Class_Custom(Model):
    def __init__(self):
        width, height = 128, 128
        num_classes = 10
        self.model = ImageClassifier(height, width, num_classes)
        path = "app/models/model_resume_10.pth"
        state_dict = torch.load(path)
        self.model.load_state_dict(state_dict)
        super().__init__()
        self.model.eval()
        print(self.model)

#    def supply_annotations(self, image_list):
#        annotations = []
#        for img in image_list:
#            label = self.model(self.model.transform(img))
#            annotation = Annotation(None, None, None, None, label)
#            annotation.box = None
#            annotations.append(annotation)
#
#        return annotations

    def load_class_dict_from_yaml(self, yaml_path):
        with open(yaml_path, 'r') as file:
            class_dict = yaml.safe_load(file)
        return class_dict
    
    def supply_annotations(self, image_list):
        mapping_dic = self.load_class_dict_from_yaml("app/models/custom_classification/class_mappings.yaml")
        rev_dic = {v : k for k, v in mapping_dic.items()}
        imdic = {}
        #print(rev_dic.keys())

        for i in range(len(image_list)):
            predictions = self.model(self.model.transform(image_list[i]))
            predictions = torch.nn.functional.softmax(predictions)
            annotations = []
            annotation = Annotation(None, None, None, None, (rev_dic[torch.argmax(predictions).item()], torch.max(predictions).item()))
            annotation.box = None
            annotations.append(annotation)

            imdic[i] = annotations
        print(imdic)

        return imdic
