import omni.ui as ui
import omni.usd
import os
from omni.ui import color as cl
from omni.kit.tool.measure import get_instance

from .model import ExtensionModel
from .style import Common_Style, ImageAndTextButton, Icon
from .menu import OptionMenu
from .tools import ExtensionTool

filepath = os.path.dirname(os.path.abspath(__file__))
label_height = 30
label_width = 150
Border_radius = 5
Margin = 5

Collapse_frame_Height = 80
class CategoryItem(ui.AbstractItem):
    """Single item of the model"""

    def __init__(self, text):
        super().__init__()
        self.name_model = ui.SimpleStringModel(text)

class CategoryModel(ui.AbstractItemModel):
    """
    Represents the list of commands registered in Kit.
    It is used to make a single level tree appear like a simple list.
    """

    def __init__(self, num, category):
        super().__init__()
        self._on_changed(num, category)

    def get_item_children(self, item):
        """Returns all the children when the widget asks it."""
        if item is not None:
            # Since we are doing a flat list, we return the children of root only.
            # If it's not root we return.
            return []

        return self.routes

    def get_item_value_model_count(self, item):
        """The number of columns"""
        return 1

    def get_item_value_model(self, item, column_id):
        """
        Return value model.
        It's the object that tracks the specific value.
        In our case we use ui.SimpleStringModel.
        """
        if item and isinstance(item, CategoryItem):
            return item.name_model

    def _on_changed(self, num, category):
        self.routes = []
        for i in range(0, num):
            Name = category[i]
            self.routes.append(CategoryItem(Name))
        self._item_changed(None)

class ExtensionUI():

    def __init__(self, controller):
        self.model = ExtensionModel(self)
        self._furni_window = ui.Window("Variant Controller")
        self._furni_window.deferred_dock_in("Console")
        self._menu_win = OptionMenu(self)
        self._menu_win.menu_window.visible = False
        self.tool = ExtensionTool(self)
        
        self.category_item = ['COMPUTER', 'CHAIR', 'MACHINE']
        self.category_model = None
        self.selected_category = None
        self.menu = None
        self.drop_helper = None
        self._stage_update = None
        
        self.chair_options = self.model.chair_variant_names
        self.monitor_options = self.model.computer_variant_names
        self.machine_options = self.model.machine_variant_names
        
        self.chair = self.model.get_variant_selection('chair')
        self.monitor = self.model.get_variant_selection('monitor')
        self.machine = self.model.get_variant_selection('machine')
        
        self.selected_variant = []
        self.selected_variantPath = []
        
        self.Area = []
        self.Floor = []
        # self.tool.Get_Area_Camera()
        # self.build_controller()
    
    def build_controller(self) -> None:
        MARGIN = 5
        with self._furni_window.frame:
            with ui.VStack():
                header_frame = ui.HStack(height=30)
                with header_frame:
                    ui.Spacer(width=MARGIN)
                    with ui.HStack(width=300):
                        ui.Label('Floor', width=50, height=25, alignment=ui.Alignment.CENTER)
                        floor_combobox = ui.ComboBox(-1, *self.Floor)
                        floor_combobox.model.add_item_changed_fn(self.on_floor_changed)
                    ui.Spacer(width=MARGIN)
                    with ui.HStack(width=300):
                        ui.Label('Area', width=50, height=25, alignment=ui.Alignment.CENTER)
                        area_combobox = ui.ComboBox(-1, *self.Area)
                        area_combobox.model.add_item_changed_fn(self.on_area_changed)
                    ui.Spacer(width=MARGIN)
                    ImageAndTextButton(
                        "Set",
                        image_path=filepath + "\data/add.svg",
                        width=80,
                        height=25,
                        image_width=14,
                        image_height=14,
                        mouse_pressed_fn=self.on_simulation_clicked,
                        tooltip = 'Set To All'
                    )
                    ui.Spacer(width=MARGIN)
                    with ui.HStack():
                        ui.Button(
                            style = Icon.MEASURE_STYLE, width=30, height=30, name='option', tooltip='Measure', 
                            alignment=ui.Alignment.RIGHT_CENTER,
                            mouse_pressed_fn=self.on_mean_tool_pressed,
                            image_url = Icon.Measure
                        )
                        ui.Spacer(width=MARGIN)
                    with ui.HStack():
                        ui.Button(
                            style=Icon.GEAR_STYLE, width=30, height=30, name='option', tooltip='Setting', 
                            alignment=ui.Alignment.RIGHT_CENTER,
                            mouse_pressed_fn=self.on_menu_pressed,
                            image_url = Icon.Gear
                        )
                        ui.Spacer(width=MARGIN)

                with ui.HStack():
                    self._Cate_frame = ui.ScrollingFrame(
                        horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
                        vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                        style=Common_Style, width=250
                    )
                    with self._Cate_frame:
                        with ui.VStack():
                            ui.Spacer(height=10)
                            self.category_model = CategoryModel(len(self.category_item), self.category_item)
                            tree_view = ui.TreeView(
                                self.category_model, root_visible=False, header_visible=False,
                                selection_changed_fn = self.on_category_selection_changed,
                                style={"TreeView.Item": {"margin_height": 4, "margin_width": 10,"font_size": 14}}
                            )      
                    self.select_area = self.build_stacks()

    def build_stacks(self) -> None:

        self._Select_frame = ui.ScrollingFrame(
            horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
            style=Common_Style,
            visible=False,
        )
        with self._Select_frame:
            self.build_pick_stack('')
    
    def build_pick_stack(self, category) -> None:
        # Variant Double Click
        def drag(url, item):
            # Draw the image and the image name in the drag tooltip
            with ui.VStack(width=101):
                ui.Image(url, width=100, height=100, alignment=ui.Alignment.H_CENTER)
                ui.Label(item, word_wrap=True, alignment=ui.Alignment.CENTER)
            return url
            
        def drag_area(item):
            url = filepath + '\data' + '/' + self.selected_category.lower() + '/' + item
            item=str(item).split('.')
            with ui.VStack(
                width=130,
                mouse_double_clicked_fn=lambda x, y, btn, flag, item=item[0]: self._on_mouse_double_clicked(btn, item)
                ):
                with ui.ZStack(height=120,):
                    image = ui.Image(url, height=120, alignment=ui.Alignment.CENTER, style_type_name_override = 'Image.Selection')
                    image.set_drag_fn(lambda: drag(url, item[0]))

                text = ui.Label(item[0], height=15, word_wrap=True, alignment=ui.Alignment.CENTER)

        with ui.VGrid(
            name='pickupArea', column_width = 130
        ):
            if category == 'Computer' or category == 'COMPUTER':
                drag_area("Desktop_Computer.png")
                drag_area("Personal_Computer.png")
                drag_area("Laptop_Free.png")
                drag_area("SamSung_Laptop.png")
            if category == 'Chair' or category == 'CHAIR':
                drag_area("Anora.png")
                drag_area("Newman.png")
                drag_area("Phineas.png")
            if category == 'Machine' or category == 'MACHINE':
                for machine in self.machine_options:
                    machine = machine+'.png'
                    drag_area(machine)
    
    def on_mean_tool_pressed(self, x, y, btn, m):
        if btn == 0 and not get_instance()._measure_panel.visible:
            get_instance()._measure_panel.visible = True
        elif get_instance()._measure_panel.visible:
            get_instance()._measure_panel.visible = False
    
    def on_area_changed(self, model, item):
        index = model.get_item_value_model().get_value_as_int()
        value = model.get_item_value_model(model.get_item_children()[index]).get_value_as_string()
        self.tool.Load_Area_Position(str(value))
        print(value)
        
    def on_floor_changed(self, model, item):
        index = model.get_item_value_model().get_value_as_int()
        value = model.get_item_value_model(model.get_item_children()[index]).get_value_as_string()
        self.tool.Load_Floor_Position(str(value))
        print(value)
        
    def on_menu_pressed(self, x, y, btn, m):
        if btn == 0 and not self._menu_win.menu_window.visible:
            self._menu_win.menu_window.visible = True
        else:
            self._menu_win.menu_window.visible = False

    def on_selected_category_changed(self, cate):
        self.selected_category = cate
        with self._Select_frame: 
            self.build_pick_stack(cate)
        self._Select_frame.visible = True
        
    def on_category_selection_changed(self, selected_items):
        for item in selected_items:
            cate = item.name_model.as_string
            self.selected_category = cate
            self.model.item_changed(cate)
            with self._Select_frame: self.build_pick_stack(cate)
            self._Select_frame.visible = True
        
    def on_simulation_clicked(self, X, Y, B, M):
        if B == 0:
            if self._menu_win.menu_value[0]:
                if self.selected_category.lower() == 'chair':
                    self.model.allchair_variants_changed(self.chair)
                if self.selected_category.lower() == 'computer':
                    self.model.allcomputer_variants_changed(self.monitor)
                if self.selected_category.lower() == 'machine':
                    self.model.allmachine_variants_changed(self.machine)
            if self._menu_win.menu_value[1]:
                self.model.all_transform_changed()
            self.model.undo.saveUndo()

    def _on_mouse_double_clicked(self, btn, item):
        if btn == 0:
            itemvariant = None
            if self.selected_category.lower() == 'chair':
                for i in self.chair_options:
                    if item.lower() in i.lower():
                        itemvariant = i
                        self.chair = itemvariant
            if self.selected_category.lower() == 'computer':
                for i in self.monitor_options:
                    if item.lower() in i.lower():
                        itemvariant = i    
                        self.monitor = itemvariant
            if self.selected_category.lower() == 'machine':
                for i in self.machine_options:
                    if item.lower() in i.lower():
                        itemvariant = i
                        self.machine = itemvariant

            if itemvariant:
                for select in self.selected_variant:
                    isSucessed = self.model.variant_changed(select, itemvariant)
                    if not isSucessed:
                        import omni.kit.notification_manager as nm
                        nm.post_notification(
                            'Not Supported! Try Another One.',
                            hide_after_timeout=True,
                        )
                        return False
                self.model.undo.saveUndo()
            else:
                print(self.selected_category)
        
    def shutdown(self):
        self.menu = None
        self._menu_win = None
        self.select_area = None 
        self.category_model = None
        self._furni_window = None
        self.model.shutdown()
        self.model = None
