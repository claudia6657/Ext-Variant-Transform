import carb.input

class KeyboardInputAction():
    
    def __init__(self, controller) -> None:
        self.modifier = None
    
    def on_input(self, event):
        control = carb.input.KeyboardInput.LEFT_CONTROL
        char = carb.input.KeyboardInput.Z
        if event.type == carb.input.KeyboardEventType.KEY_PRESS:
            if event.input == control:
                self.modifier = control
                print('CTRL')
            
            if event.input == char:
                print('Z')
                if self.modifier:
                    print('CTRL + Z')
        
        if event.type == carb.input.KeyboardEventType.KEY_RELEASE:
            self.modifier = None