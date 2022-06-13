from pynput.mouse import Controller, Listener

mouse = Controller()
isAimbotOn = False


def on_click(x, y, button, pressed):
    global isAimbotOn
    if pressed and button == button.x2:
        isAimbotOn = not isAimbotOn

listener = Listener(
    on_click=on_click
)
listener.start()

def aimAt(aims, x, y):
    if not isAimbotOn: return
    mouse_x, mouse_y = mouse.position
    dists = []
    closest_idx = 0
    closest_dist = 99999
    for idx, det in enumerate(aims):
        _, x_c, y_c, _, _ = det
        distance = (x * float(x_c) - mouse_x) ** 2 + (y * float(y_c) - mouse_y) ** 2
        if distance < closest_dist:
            closest_idx = idx
            closest_dist = distance

    det = aims[closest_idx]
    tag, bbox_center_x, bbox_center_y, width, height = det
    x_center, width = x * float(bbox_center_x), x * float(width)
    y_center, height = y * float(bbox_center_y), y * float(height)
    tag == int(tag)
    mouse.position = (x_center, y_center)
