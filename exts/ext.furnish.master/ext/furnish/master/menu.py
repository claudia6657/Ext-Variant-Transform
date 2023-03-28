import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window

from .style import POPUP_MENU_STYLE

class OptionMenu():
    
    def __init__(self, controller):
        self.controller = controller
        pos = [get_active_viewport_window().frame.computed_content_width, get_active_viewport_window().frame.computed_content_height]
        self.menu_window = ui.Window('menu', width=200, height=120, style=POPUP_MENU_STYLE)
        self.menu_window.flags = ui.WINDOW_FLAGS_NO_COLLAPSE|ui.WINDOW_FLAGS_NO_RESIZE|ui.WINDOW_FLAGS_NO_TITLE_BAR
        self.menu_window.setPosition(740, pos[1]+90)
        self.menu_item = ['Variant Items', 'Transform Translation', 'Transform Rotation']
        self.menu_value = [True, True, True]
        self.build_menu()
    
    def build_menu(self):
        with self.menu_window.frame:
            with ui.VStack():
                ui.Label('Set Options', height=30)
                ui.Separator(height=5)
                content = []
                with ui.HStack(height=20, alignmemt=ui.Alignment.LEFT_TOP, style={"margin_hieght":2}):
                    checkbox = ui.CheckBox(width=30)
                    label = ui.Label(self.menu_item[0], alignmemt=ui.Alignment.LEFT_CENTER, name=self.menu_item[0])
                    content.insert(0, self.menu_item[0])
                    checkbox.model.set_value(self.menu_value[0])
                    checkbox.model.add_value_changed_fn(lambda check: self.check_menu_value(content[0], check.get_value_as_bool()))
                with ui.HStack(height=20, alignmemt=ui.Alignment.LEFT_TOP, style={"margin_hieght":2}):
                    checkbox = ui.CheckBox(width=30)
                    label = ui.Label(self.menu_item[1], alignmemt=ui.Alignment.LEFT_CENTER, name=self.menu_item[1])
                    content.insert(1, self.menu_item[1])
                    checkbox.model.set_value(self.menu_value[1])
                    checkbox.model.add_value_changed_fn(lambda check: self.check_menu_value(content[1], check.get_value_as_bool()))
                with ui.HStack(height=20, alignmemt=ui.Alignment.LEFT_TOP, style={"margin_hieght":2}):
                    checkbox = ui.CheckBox(width=30)
                    label = ui.Label(self.menu_item[2], alignmemt=ui.Alignment.LEFT_CENTER, name=self.menu_item[2])
                    content.insert(2, self.menu_item[2])
                    checkbox.model.set_value(self.menu_value[2])
                    checkbox.model.add_value_changed_fn(lambda check: self.check_menu_value(content[2], check.get_value_as_bool()))
    
    def check_menu_value(self, content, value):
        for i in range(len(self.menu_item)):
            if content == self.menu_item[i]:
                self.menu_value[i] = value 
        