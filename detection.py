import torch
import numpy as np

from models.common import DetectMultiBackend
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils.augmentations import letterbox

from options import opt

# Load model
model = DetectMultiBackend(opt.weights, device=opt.device, dnn=False, data=opt.data, fp16=opt.half)

# Run inference
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size(opt.imgsz, s=stride)  # check image size
model.warmup(imgsz=(1, 3, *imgsz))  # warmup


def detection(img0):
    img = letterbox(img0, imgsz, stride=stride)[0]
    img = img.transpose((2, 0, 1))[::-1]
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(opt.device)
    img = img.half() if model.fp16 else img.float()
    img /= 255  # normalize to 0.0-1.0
    if len(img.shape) == 3:
        img = img[None]
    prediction = model(img, augment=False, visualize=False)
    # NMS
    prediction = non_max_suppression(prediction,
                                     opt.conf_thres,
                                     opt.iou_thres,
                                     agnostic=False)  # filtered prediction results
    # Process predictions
    aims = []
    for i, det in enumerate(prediction):  # per image
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class

            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = (cls, *xywh)  # label format
                # Labels: 'CT' == 0, 'CT_HEAD', 'T', 'T_HEAD'
                aim = ('%g ' * len(line)).rstrip() % line + '\n'
                aim = aim.split(' ')
                aims.append(aim)

    return aims
