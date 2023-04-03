import torch
from yolov5.models.experimental import attempt_load
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression

from Helpers import scale_coords
from Helpers import plot_one_box
from Helpers import preprocess


#initialize model with null


class Model:
    def __init__(self):
        self.model = None
        self.img_size = 640

    def loadModel(self):
        self.model = attempt_load('Model/weight.pt', map_location=torch.device('cpu'))

    def pred_annot(self, frame: object) -> object:
        img = preprocess(frame, [self.img_size,self.img_size], letter_box=True)

        # Convert image to Torch tensor
        img = torch.from_numpy(img).to('cpu')

        # Add batch dimension
        img = img.unsqueeze(0)

        pred = self.model(img)[0]

        pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.5)[0]

        # Draw boxes on the original frame
        if pred is not None:
            pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], frame.shape).round()

            for *xyxy, conf, cls in pred:
                label = f'{self.model.names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=3)

        return frame

