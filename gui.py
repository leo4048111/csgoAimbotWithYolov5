import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
from options import opt


def impl_glfw_init(window_name="csgo-detect settings", width=300, height=230):
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
            imgui.text("Display Scale:")
            if imgui.radio_button("1.25", opt.display_scale == 1.25): opt.display_scale = 1.25
            imgui.same_line()
            if imgui.radio_button("1.00", opt.display_scale == 1.00): opt.display_scale = 1.00
            imgui.same_line()
            if imgui.radio_button("1.50", opt.display_scale == 1.50): opt.display_scale = 1.50
            imgui.same_line()
            if imgui.radio_button("1.75", opt.display_scale == 1.75): opt.display_scale = 1.75
            imgui.text("Hitbox:")
            clicked, state = imgui.checkbox("CT", 0 in opt.hitbox)
            if clicked and state:
                opt.hitbox.append(0)
            elif clicked and not state:
                opt.hitbox.remove(0)
            imgui.same_line()
            clicked, state = imgui.checkbox("CT_HEAD", 1 in opt.hitbox)
            if clicked and state:
                opt.hitbox.append(1)
            elif clicked and not state:
                opt.hitbox.remove(1)
            imgui.same_line()
            clicked, state = imgui.checkbox("T", 2 in opt.hitbox)
            if clicked and state:
                opt.hitbox.append(2)
            elif clicked and not state:
                opt.hitbox.remove(2)
            imgui.same_line()
            clicked, state = imgui.checkbox("T_HEAD", 3 in opt.hitbox)
            if clicked and state:
                opt.hitbox.append(3)
            elif clicked and not state:
                opt.hitbox.remove(3)
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
