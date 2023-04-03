import torch
from yolov5.models.experimental import attempt_load
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression

from Helpers import scale_coords
from Helpers import plot_one_box
from Helpers import preprocess

from yolov5.utils.plots import Annotator, colors
import numpy as np
import cv2


class Model:
    def __init__(self):
        #self.model = attempt_load('Model/weight.pt', device=torch.device('cpu'))
        self.model = torch.hub.load('./yolov5', 'custom', path='./Model/weight.pt', source='local')
        self.img_size = 640

    def pred_annot(self, frame):

        img = frame

        pred = self.model(img, size=640)

        # pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45, classes=None, agnostic=False, max_det=0.3)

        res = pred.pandas().xyxy[0].to_json(orient="records")

        print(res)



        #TODO:annotate the frame

        # annotator = Annotator(img, line_width=3, example=str(self.model.names))
        # for i, det in enumerate(pred):
        #     if len(det):
        #         for *xyxy, conf, cls in reversed(det):
        #             c = int(cls)  # integer class
        #             label = None if False else (self.model.names[c] if False else f'{self.model.names[c]} {conf:.2f}')
        #             annotator.box_label(xyxy, label, color=colors(c, True))
        #
        # img = annotator.result()
        #return the frame
        # return img

        # pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.5)[0]
        #
        # # Draw boxes on the original frame
        # if pred is not None:
        #     pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], frame.shape).round()
        #
        #     for *xyxy, conf, cls in pred:
        #         label = f'{self.model.names[int(cls)]} {conf:.2f}'
        #         plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=3)
        #
        # cv2.imshow(img)

