import torch
import cv2

class Model:
    def __init__(self):
        # self.model = attempt_load('Model/weight.pt', device=torch.device('cpu'))
        self.model = torch.hub.load('./yolov5', 'custom', path='./Model/weight.pt', source='local')
        self.img_size = 640

    def pred_annot(self, frame):
        img = frame

        pred = self.model(img, size=640)

        # pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45, classes=None, agnostic=False, max_det=0.3)

        res = pred.pandas().xyxy[0].to_json(orient="records")
        count = pred.pandas().xyxy[0].shape[0]
        # TODO calculate count for emergency and non emergency both

        # print(res)
        # Output:
        # [{"xmin":365.4317321777,"ymin":170.4187011719,"xmax":375.5906066895,"ymax":178.2403564453,"confidence":0.2531405985,"class":1,"name":"car"}]

        for bbox in pred.xyxy[0]:
            xmin, ymin, xmax, ymax = bbox[:4]
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 4)

        return [[count, 0], frame]  # returns unnanoted frame for now for checking purposes and [count, 0] for testing purposes

        # TODO@irtiza:annotate the frame and return it instead of the original frame