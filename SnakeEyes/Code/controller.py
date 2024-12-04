from SnakeEyes.Code.settings import Settings

import pygame
class Controller:
    def __init__(
        self, controller_type="keyboard", controller_ID=None, controller_scheme=None
    ):
        self.controller_type = controller_type  # 'keyboard' or 'joystick'
        self.controller_ID = controller_ID  # Joystick ID if using a controller
        self.controller_scheme = controller_scheme
        self.joystick = None

        if self.controller_type == "joystick" and controller_ID is not None:
            self.joystick = pygame.joystick.Joystick(controller_ID)

        self.define_controls()

    def get_joystick_id(self):
        if self.joystick:
            return self.joystick.get_instance_id()
        return None

    def define_controls(self):
        if self.controller_type == "joystick":
            self.axis_horizontal = 0
            self.axis_vertical = 1
            self.action_buttons = {"ready": 0, "space": 1, "BRight": 10, "BLeft": 9}
        elif self.controller_type == "keyboard":
            self.map_keyboard_controls()

    def map_keyboard_controls(self):
        if not self.controller_scheme:
            print(f"Error: No control scheme provided for keyboard controller.")
            self.controller_scheme = "WASD"

        # DEBUG STATEMENT
        # print(f"Mapping controls for: {self.controller_scheme}")

        control_schemes = {
            "WASD": {
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "ready": pygame.K_1,
                "space": pygame.K_SPACE,
            },
            "TFGH": {
                "up": pygame.K_t,
                "down": pygame.K_g,
                "left": pygame.K_f,
                "right": pygame.K_h,
                "ready": pygame.K_3,
                "space": pygame.K_SPACE,
            },
            "IJKL": {
                "up": pygame.K_i,
                "down": pygame.K_k,
                "left": pygame.K_j,
                "right": pygame.K_l,
                "ready": pygame.K_5,
                "space": pygame.K_SPACE,
            },
            "Arrows": {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "ready": pygame.K_7,
                "space": pygame.K_SPACE,
            },
        }

        scheme = control_schemes.get(self.controller_scheme)

        if scheme:
            self.up = scheme["up"]
            self.down = scheme["down"]
            self.left = scheme["left"]
            self.right = scheme["right"]
            self.action_buttons = {
                "ready": scheme["ready"],
                "space": scheme["space"]
            }
        else:
            print(f"Error: Unknown control scheme '{self.controller_scheme}'")

    def get_movement(self):
            if self.controller_type == "keyboard":
                keys = pygame.key.get_pressed()
                x_movement = 0
                y_movement = 0
                if keys[self.left]:
                    x_movement -= 1
                if keys[self.right]:
                    x_movement += 1
                if keys[self.up]:
                    y_movement -= 1
                if keys[self.down]:
                    y_movement += 1

                length = (x_movement**2 + y_movement**2) ** 0.5
                if length > 0:
                    x_movement /= length
                    y_movement /= length
                return x_movement, y_movement

            elif self.controller_type == "joystick":
                x_axis = self.joystick.get_axis(self.axis_horizontal)
                y_axis = self.joystick.get_axis(self.axis_vertical)

                deadzone = Settings.CONTROLLER_DEADZONE
                if abs(x_axis) < deadzone:
                    x_axis = 0
                if abs(y_axis) < deadzone:
                    y_axis = 0
                return x_axis, y_axis

    def is_action_pressed(self, action_name):
        if self.controller_type == "keyboard":
            keys = pygame.key.get_pressed()
            return keys[self.action_buttons[action_name]]
        elif self.controller_type == "joystick":
            button_ID = self.action_buttons[action_name]
            # DEBUG STATEMENT
            # print(button_ID)
            return self.joystick.get_button(button_ID)