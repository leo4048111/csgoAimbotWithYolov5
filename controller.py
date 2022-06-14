from pynput.mouse import Controller, Listener
from options import opt

mouse = Controller()


def on_click(x, y, button, pressed):
    if pressed and button == button.x2:
        opt.aimbot_status = not opt.aimbot_status

listener = Listener(
    on_click=on_click
)
listener.start()


def aimAt(aims, x, y):
    if not opt.aimbot_status: return
    x = x * opt.display_scale
    y = y * opt.display_scale
    mouse_x, mouse_y = mouse.position
    dists = []
    closest_idx = -1
    closest_dist = 99999
    for idx, det in enumerate(aims):
        tag, x_c, y_c, _, _ = det
        if int(tag) not in opt.hitbox:
            continue
        distance = (x * float(x_c) - mouse_x) ** 2 + (y * float(y_c) - mouse_y) ** 2
        if distance < closest_dist:
            closest_idx = idx
            closest_dist = distance

    if closest_idx == -1:
        return
    det = aims[closest_idx]
    tag, bbox_center_x, bbox_center_y, width, height = det
    x_center, width = x * float(bbox_center_x), x * float(width)
    y_center, height = y * float(bbox_center_y), y * float(height)
    mouse.position = (x_center, y_center)
