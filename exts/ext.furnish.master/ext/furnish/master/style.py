from omni import ui
from omni.ui import color as cl
from functools import partial
import os
filepath = os.path.dirname(os.path.abspath(__file__))

label_height = 30
label_width = 150
Border_radius = 3
Margin = 5

Collapse_frame_Height = 80
class Colors:
    Background = ui.color.shade(0xFF23211F, light=0xFF535354)
    Scrollbar = ui.color.shade(0xFF808080, light=0xFF9E9E9E)
    Selected = ui.color.shade(0xFFFFC734, light=0xFFC5911A)
    Text = ui.color.shade(0xFFA1A1A1, light=0xFFE0E0E0)
    DarkText = ui.color.shade(0xFF504F50, light=0xFFA1A1A1)
    ImageDisable = ui.color.shade(0xFF696969)
    Hover = ui.color.shade(0xFFF4F9FE)
    ResetInvalid = ui.color.shade(0xFF505050)
    Reset = ui.color.shade(0xFFA07D4F)
    Line = ui.color.shade(0x338A8777)
    CLR_Label = 0xFFE2E2E2
    CLR_Disabled = 0xFFFFFFFF
    Window = ui.color.shade(0xFF353535)
    Hint = ui.color.shade(0xFF6A6A6A)
    Warn = ui.color.shade(0xCC2222FF)
    Image = ui.color.shade(0xFFA8A8A8)

class Icon:
    Gear =  filepath + "\data\gear.svg"
    Measure = filepath + "\data\measure.svg"
    Save = filepath + "\data\save.svg"
    User = filepath + "\data\menu_refresh.svg"
    
    GEAR_STYLE = {
        "Button":{"background_color": 0x00000000},
        "Button:hovered":{"background_color": 0xFF333333}
    }
    MEASURE_STYLE = {
        "Button":{"background_color": 0x00000000},
        "Button:hovered":{"background_color": 0xFF333333}
    }
    SAVE_STYLE = {
        "Button":{"background_color": 0x00000000},
        "Button:hovered":{"background_color": 0xFF333333}
    }
    

POPUP_MENU_STYLE = {
    "Window": {"background_color": 0xFF232323, "padding": 0, "margin": 0},
}

CollapsableControlFrameStyle = {
    "CollapsableFrame": {
        "background_color": 0xFF333333,
        "secondary_color": 0xFF333333,
        "color": 0xFFCE9600,
        "border_radius": Border_radius,
        "border_width": 0,
        "font_size": 14,
        "padding": Margin * 2,
        "margin_width": Margin,
        "margin_height": 2,
    },
    "ComboBox": {"color": Colors.CLR_Label, "background_color": 0xFF23211F, "secondary_color": 0xFF23211F, "border_radius": 2},
    "ComboBox:disabled": {"color": Colors.CLR_Disabled},
}

TreeViewFrameStyle = {
    "ComboBox": {"color": Colors.CLR_Label, "background_color": 0xFF23211F, "secondary_color": 0xFF23211F, "border_radius": 2},
    "ComboBox:disabled": {"color": Colors.CLR_Disabled},
}

Common_Style = {
    "ScrollingFrame":{
        "background_color": 0xFF232323, 
        "border_radius": 1, 
        "border_width": 1, 
        "border_color": 0xFFFFFFFF, 
        "padding": 2,
        "margin_width":2
    },
    "HStack::pickupArea":{"padding_width": 1},
    "Label::Description": {"font_size": 20, "margin_width":Margin},
    "Label::smallDescription": {"font_size": 16, "margin_width":Margin},
    "Label::TITLE":{"font_size": 20, "margin_width":5},
    "Label::SUBTITLE":{"font_size": 14, "margin_width":5},
    "Image":{"margin_width":0.5, "margin_height":0.5},
    "Label":{"margin_width":1, "margin_height":1},
    "Line":{"color": 0xFFD3D3D3},
    "Button::option":{"margin_width":5},
    "Image.Selection":{"border_radius": 3,"border_width": 0,"border_color": 0},
    "Image.Selection:selected":{"border_radius": 3,"border_width": 1,"border_color": 0xFFFFFFFF}
}

Item_Block = {
    "VStack.Image":{
        "border_radius": 10,
        "border_width": 5,
        "border_color": 0xFFFFFFFF,
    }
}

User_Enter_Style={
    "Label::title":{
        "font_size": 20,
        "color": 0xFFFFFFFF,
    },
    "Label":{
        "font_size": 18,
        "color": 0xFFD3D3D3
    },
    "Button":{
        "margin_width":120,
        "color": 0xFFFFFFFF,
        "background_color": 0x10000000
    },
    "Line":{
        "color": 0xFFD3D3D3
    }
}

Save_Window_Style={
    "Label::title":{
        "font_size": 20,
        "color": 0xFFFFFFFF,
    },
    "Label::command_Field":{
        "font_size": 16,
        "margin_height":5
    },
    "Button":{
        "margin_width":5,
        "color": 0xFFFFFFFF,
        "background_color": 0x10000000
    },
    "Line":{
        "color": 0xFFD3D3D3
    },
    "StringField":{
        "margin_height":5,
    }
}

History_Frame_Style={
    "ScrollingFrame":{
        "background_color": 0xFF232323, 
        "border_radius": 1, 
        "border_width": 1, 
        "border_color": 0xFFFFFFFF, 
        "padding": 2,
        "margin_width":5,
        "margin_height": 1
    },
    "ScrollingFrame::add":{
        "background_color": 0xFF2F2F2F, 
        "border_width": 1, 
        "border_color": 0xFFFFFFFF, 
        "padding": 2,
        "margin_width":2,
        "margin_height": 4
    },
    "ScrollingFrame:hovered":{
        "background_color": 0xFF999999, 
        "border_width": 1, 
        "border_color": 0xFFFFFFFF, 
        "padding": 2,
        "margin_width":2,
        "margin_height": 4,
    },
    "Label::name":{
        "font_size": 16,
        "margin_width": 5
    },
    "Label::time":{
        "font_size": 20,
        "margin_width": 5
    },
    "Line":{"color": 0xFFD3D3D3}
}

def show_tooltip(label):
    """Show a tooltip.

    Use this callback to avoid issues with the tooltip inheriting style
    (in particular margin/padding) from parent widgets.
    """
    ui.Label(
        label,
        style={
            "color": 0xFF585A51,
            "background_color": 0xFFCAF5FB,
            "margin": 2,
            "padding": 4,
        },
    )
    return

class ImageAndTextButton(ui.ZStack):
    """Hack class to allow centering an icon and text in a Button."""

    def __init__(self, label, width, height, image_path, image_width, image_height, mouse_pressed_fn, tooltip):

        super().__init__(width=width, height=height, style={"margin": 1, "padding": 1})

        with self:

            # Add a button with a blank space for the label - this ensures it respects the
            # height
            ui.Button(
                " ",
                width=ui.Percent(100),
                height=height,
                mouse_pressed_fn=mouse_pressed_fn,
                tooltip_fn=partial(show_tooltip, tooltip),
            )

            # HStack with an image and label
            with ui.HStack(width=ui.Percent(100)):
                ui.Spacer()
                im = ui.Image(image_path, width=image_width)
                ui.Spacer(width=ui.Pixel(4))
                ui.Label(label, width=0)
                ui.Spacer()