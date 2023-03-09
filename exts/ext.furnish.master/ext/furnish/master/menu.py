import omni.ui as ui

class OptionMenu():
    
    def __init__(self, controller):
        self.menu_window = ui.Window('menu', width=200, height=300)
        menu_item = ['a', 'b']
        self.build_menu(menu_item)
    
    def build_menu(self, menuItem):
        print('build menu?')
        with self.menu_window.frame:
            with ui.VStack():
                ui.Label('Set Options')
                ui.Separator()
                for i in menuItem:
                    with ui.HStack():
                        ui.CheckBox()
                        ui.Label(i)
                
            
