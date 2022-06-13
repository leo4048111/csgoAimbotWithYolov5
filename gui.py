import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
from options import opt


def impl_glfw_init(window_name="csgo-detect settings", width=300, height=400):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.set_window_attrib(window, glfw.FLOATING, True)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


class GUI(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0, 0, 0, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        self.side = ['CT', 'T']
        self.side_idx = 0

    def loop(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()
            imgui.begin("csgo-detect settings", True)

            imgui.text("Software is up and running...")

            imgui.text("Aimbot status: " + ('[ON]' if opt.aimbot_status else '[OFF]'))

            _, opt.conf_thres = imgui.slider_float("conf-thres", opt.conf_thres, 0.01, 0.99)
            _, opt.iou_thres = imgui.slider_float("iou-thres", opt.iou_thres, 0.01, 0.99)
            _, self.side_idx = imgui.combo(opt.side, self.side_idx, self.side)
            opt.side = self.side[self.side_idx]
            imgui.end()

            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

def gui_main():
    GUI().loop()

if __name__ == "__main__":
    gui_main()