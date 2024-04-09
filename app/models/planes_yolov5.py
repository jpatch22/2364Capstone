from app.models.model import Model
from app.Annotation import Annotation

import os
import sys
from pathlib import Path
import torch
import numpy as np

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
# from planes_yolov5.utils.dataloaders import LoadImages
from utils.general import (
    Profile,
    check_img_size,
    non_max_suppression,
)
from utils.torch_utils import select_device

class Planes_Model(Model):
    def __init__(self):
        super().__init__()
        weights = "app\\models\\best.pt"
        imgsz = 2560
        
        # Load model in init for faster inference
        self.device = select_device("") # defice is emptystring by default in detect.py
        self.model = DetectMultiBackend(weights, device=self.device, dnn=False, data=None, fp16=False) #data = path to data??
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        
        
    def supply_annotations(self, image_list):
        # image_list is just a single PIL Image
        annotations = []
        
        conf_thres = 0.4
        
        # Default Values
        augment = False
        iou_thres = 0.45
        bs = 1  # batch_size
        classes = None
        agnostic_nms = False
        max_det = 1000 # maximum detections per image        

        # Run inference
        self.model.warmup(imgsz=(1 if self.pt or self.model.triton else bs, 3, self.imgsz))  # warmup; removed *
        seen, windows, dt = 0, [], (Profile(device=self.device), Profile(device=self.device), Profile(device=self.device))
            
        # for im in image_list:
        im = image_list
        origWidth, origHeight = im.size
        # print(type(im)) # Its a PIL image
        im2 = im.resize((self.imgsz, self.imgsz))
        im = np.array(im2)
        
        with dt[0]:
            im = torch.from_numpy(im).to(self.model.device)
            im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            if self.model.xml and im.shape[0] > 1:
                ims = torch.chunk(im, im.shape[0], 0)
                
        # Encountered same error from land use dataset. Need to "rotate".
        im = im.permute(0, 3, 1, 2)

        # Inference
        with dt[1]:
            visualize = False # increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            if self.model.xml and im.shape[0] > 1:
                pred = None
                for image in ims:
                    if pred is None:
                        pred = self.model(image, augment=augment, visualize=visualize).unsqueeze(0)
                    else:
                        pred = torch.cat((pred, self.model(image, augment=augment, visualize=visualize).unsqueeze(0)), dim=0)
                pred = [pred, None]
            else:
                pred = self.model(im, augment=augment, visualize=visualize)
        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        
        # Process predictions
        for i, det in enumerate(pred):  # per image

            if len(det):
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    confidence = float(conf)
                    confidence_str = f"{confidence:.2f}"
                    annotBox = []
                    
                    for idx in range(len(xyxy)):
                        coord = xyxy[idx].item()
                        
                        if idx % 2 == 0:
                            annotBox.append(coord * origWidth / self.imgsz)
                        else:
                            annotBox.append(coord * origHeight / self.imgsz)

                    annotations.append(Annotation(annotBox[0], annotBox[1], annotBox[2], annotBox[3], ("Aircraft; conf=" + confidence_str)))

        for annot in annotations:
            print(annot.label, ", location: ", annot.box)
        print("Found {} Annotations".format(len(annotations)))

        return annotations
    