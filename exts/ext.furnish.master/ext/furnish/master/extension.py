import omni.ext
import omni.usd
import omni.kit.app
import carb

from .ui import ExtensionUI
from .model import ExtensionModel
from .history_window import HistoryUI
from .layer_controller import LayerController

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
    
    #======================================
    # Events
    #======================================
    def on_click_user_enter(self):
        self._layer.user = self._hisui.user
        set_layer = self._layer.set_layer_by_user()
        '''Return False if no this user's layer'''
        if set_layer:
            self._hisui._user_window.visible = False
            self._hisui.build_history()
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
        usd_context = omni.usd.get_context()
        stage = usd_context.get_stage()
        prim_paths = usd_context.get_selection().get_selected_prim_paths()
        if 'Chair' in prim_paths[0]:
            self._ui.selected_variant = []
            for i in self._ui.model.chairVariantList:
                path = str(i.GetPath()).split('/OmniVariants')[0]
                print(path)
                if path in prim_paths[0]:
                    self._ui.selected_variant.append(i)
                    print('yes')
                    break
        if 'Computer' in prim_paths[0]:
            self._ui.selected_variant = []
            for i in self._ui.model.computorVariantList:
                path = str(i.GetPath()).split('/OmniVariants')[0]
                print(path)
                if path in prim_paths[0]:
                    self._ui.selected_variant.append(i)
                    print('yes')
                    break
        if 'machine' in prim_paths[0]:
            for i in self._ui.model.machineVariantList:
                path = str(i.GetPath())
                
                if path in prim_paths[0]:
                    index = self._ui.model.machineVariantList.index(i)
                    self._ui.selected_variant.append(i)
                    self._ui.model.transform.insert(2,self._ui.model.Get_VariantItem_transform(self._ui.model.machinePath[index]))
                    select = self._ui.model.machinePath[index].split('OmniVariants')[0]
                    selection = usd_context.get_selection().set_selected_prim_paths([select], True)
                    break
        print(self._ui.selected_variant)
        
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
