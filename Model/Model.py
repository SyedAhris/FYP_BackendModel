import torch
import cv2

class Model:
    def __init__(self):
        # self.model = attempt_load('Model/weight.pt', device=torch.device('cpu'))
        self.model = torch.hub.load('./yolov5', 'custom', path='./Model/Weights/best_5l_v11.pt', source='local')
        self.img_size = 640

    def pred_annot(self, frame):
        img = frame

        pred = self.model(img, size=640)

        # pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45, classes=None, agnostic=False, max_det=0.3)

        res = pred.pandas().xyxy[0].to_json(orient="records")
        count = pred.pandas().xyxy[0].shape[0]
        # TODO@irtiza  calculate count for emergency and non emergency both

        #print(res)
        # Output:
        # [{"xmin":370.8471984863,"ymin":280.0169067383,"xmax":403.8054504395,"ymax":326.3619995117,"confidence":0.2662596405,"class":0,"name":"Emergency"}]

        for bbox in pred.xyxy[0]:
            xmin, ymin, xmax, ymax, conf, cls = bbox.tolist()
            color = (0, 255, 0) if cls == 0 else (0, 0, 255)  # Green for non-emergency, Red for emergency
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
            cv2.putText(frame, f"{conf:.2f}", (int(xmin), int(ymin - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return [[count, 0], frame]  # returns unnanoted frame for now for checking purposes and [count, 0] for testing purposes

        # TODO@Irtiza send back the 2 counts values Non Emergency followed by Emergency [[NonEmegency, Emergency], frame]