import argparse
import os
import sys

from pathlib import Path

from utils.torch_utils import select_device

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'CS2W.pt', help='model path(s)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/mydata.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--half', default=False, help='whether to use model.half()')
    parser.add_argument('--aimbot-status', default=True, help='whether aimbot is on')
    parser.add_argument('--hitbox', default=[0, 1, 2, 3], help='The aimbot will aim at the specific positions')
    parser.add_argument('--display-scale', type=float, default=1.25, help='The Scale value in display setting' )
    parser.add_argument('--detection-region-width', type=int, default=1065, help='Detection region width' )
    parser.add_argument('--detection-region-height', type=int, default=728, help='Detection region height' )


    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    opt.device = select_device(opt.device)
    opt.half = (opt.device != 'cpu')  # if device is cpu use model.half()

    return opt


opt = parse_opt()
