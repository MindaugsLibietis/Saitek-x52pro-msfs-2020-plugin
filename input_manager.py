import pygame

class X52Input:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joy = None

        if pygame.joystick.get_count() > 0:
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
            print(f"DirectInput connected to: {self.joy.get_name()}")
        else:
            print("No Joystick detected by DirectInput!")

    def get_active_button(self):
        """Returns the ID of the button currently being pressed, or None."""
        if not self.joy: return None

        # We must 'pump' events to get fresh data from Windows
        pygame.event.pump()

        for i in range(self.joy.get_numbuttons()):
            if self.joy.get_button(i):
                return i
        return None