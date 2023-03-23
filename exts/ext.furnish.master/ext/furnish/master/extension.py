import omni.ext
import omni.usd
import omni.kit.app
import carb
import carb.input

from .ui import ExtensionUI
from .model import ExtensionModel
from .history_window import HistoryUI
from .layer_controller import LayerController
from .keyboardInput import KeyboardInputAction
class ExtFurnishMasterExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        if omni.usd.get_context().get_stage() is None:
            # Workaround for running within test environment.
            omni.usd.get_context().new_stage()

        self._stage_event_sub = omni.usd.get_context().get_stage_event_stream().create_subscription_to_pop(
            self._on_stage_event, name="Stage Open/Closing Listening"
        )        
        self._ui = ExtensionUI(self)
        self._hisui = HistoryUI(self)
        self._layer = LayerController(self)
        self.key = KeyboardInputAction(self)
                
        appwindow = omni.appwindow.get_default_app_window()
        keyboard = appwindow.get_keyboard()
        input = carb.input.acquire_input_interface()
        self._keyboard_sub_id = input.subscribe_to_keyboard_events(keyboard, self.key.on_input)
    
    #======================================
    # Events
    #======================================
    def on_click_user_enter(self):
        self._layer.user = self._hisui.user
        set_layer = self._layer.set_layer_by_user()
        '''Return False if no this user's layer'''
        if set_layer or self._layer.tempLayer:
            self._hisui._user_window.visible = False
            self._hisui.build_history()
            self._ui.tool.Get_Area_Camera()
            self._ui.tool.Get_Floor_Camera()
            self._ui.build_controller()
        else:
            self._hisui._user_window.visible = False
            def add_new_user():
                self._layer.create_newUserLayer()
                self.on_click_user_enter()
            def cancel():
                self._hisui._user_window.visible = True
                
            import omni.kit.notification_manager as nm
            nm.post_notification(
                'First time here? Do you want to create new scene?',
                hide_after_timeout=False,
                button_infos=[
                    nm.NotificationButtonInfo("YES", on_complete=add_new_user),
                    nm.NotificationButtonInfo("CANCEL", on_complete=cancel),
                ]
            )
    
    def _on_kit_selection_changed(self):
        # Execute if Selection changed
        usd_context = omni.usd.get_context()
        prim_paths = usd_context.get_selection().get_selected_prim_paths()
        category = None
        multiSelect = False

        def recount(variantList, pathList, selected, trans):
            for i in variantList:
                path = str(i.GetPath())
                
                if path in selected:
                    index = variantList.index(i)
                    self._ui.selected_variant.append(i)
                    self._ui.model.transform.insert(trans,self._ui.model.Get_VariantItem_transform(pathList[index]))
                    select = pathList[index].split('/OmniVariants')[0]
                    self._ui.selected_variantPath.append(select)
                    selection = usd_context.get_selection().set_selected_prim_paths(self._ui.selected_variantPath, True)
                    self._ui.model.newTransform[trans] = select
                    break
        
        for selected in prim_paths:
            if selected in self._ui.selected_variantPath:
                multiSelect = True
                
            if 'Chair' in selected:
                if category != 'Chair' and not multiSelect:
                    self._ui.selected_variant = []
                    self._ui.selected_variantPath = []
                category = 'Chair'
                recount(self._ui.model.chairVariantList, self._ui.model.chairPath, selected, 0)
                self._ui.on_selected_category_changed('CHAIR')

            if 'Computer' in selected:
                if category != 'Computer' and not multiSelect:
                    self._ui.selected_variant = []
                    self._ui.selected_variantPath = []
                category = 'Computer'
                recount(self._ui.model.computorVariantList, self._ui.model.computerPath, selected, 1)
                self._ui.on_selected_category_changed('COMPUTER')
                
            if 'Machine' in selected:
                if category != 'Machine' and not multiSelect:
                    self._ui.selected_variant = []
                    self._ui.selected_variantPath = []
                category = 'Machine'
                recount(self._ui.model.machineVariantList, self._ui.model.machinePath, selected, 2)
                self._ui.on_selected_category_changed('MACHINE')
    
    def unsubscribe(self):
        if self._stage_event_sub:
            self._stage_event_sub.unsubscribe()
            self._stage_event_sub = None
        
    def _on_stage_event(self, event: carb.events.IEvent):
        """Called on USD Context event"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            self._on_kit_selection_changed()
        if event.type == int(omni.usd.StageEventType.CLOSING):
            self.unsubscribe()
            self._ui.shutdown()
            self._ui = None
            self._hisui.shutdown()
            self._hisui = None
            self._layer.shutdown()
            self._layer = None
            # self.model = None
            if self._stage_event_sub:
                self._stage_event_sub.unsubscribe()
                self._stage_event_sub = None
        
    def on_shutdown(self):
        self.unsubscribe()
        if self._ui:
            self._ui.shutdown()
        if self._hisui:
            self._hisui.shutdown()
        if self._layer:
            self._layer.shutdown()
        self._ui = None
        self._hisui = None
        self._layer = None
        
        # self.model = None
        if self._stage_event_sub:
            self._stage_event_sub.unsubscribe()
            self._stage_event_sub = None
        
        appwindow = omni.appwindow.get_default_app_window()
        keyboard = appwindow.get_keyboard()
        input = carb.input.acquire_input_interface()
        input.unsubscribe_to_keyboard_events(keyboard, self._keyboard_sub_id)
