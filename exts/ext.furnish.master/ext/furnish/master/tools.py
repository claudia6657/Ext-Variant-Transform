import omni.usd
from omni.kit.viewport.utility import get_active_viewport

CameraScope = '/World/Area'

class ExtensionTool():
    
    def __init__(self, controller) -> None:
        self.controller = controller
    
    def Get_Area_Camera(self):
        stage = omni.usd.get_context().get_stage()
        basePrim = stage.GetPrimAtPath(CameraScope)
        
        for i in basePrim.GetChildren():
            self.controller.Area.append(i.GetName())
        
        return True
    
    def Change_Active_Camera(self, camera_path):
        viewport = get_active_viewport()

        if not viewport:
            raise RuntimeError("No active Viewport")

        viewport.camera_path = camera_path
        
    def Load_Area_Position(self, path_name):
        stage = omni.usd.get_context().get_stage()

        user_camera = CameraScope+'/User'
        self.Change_Active_Camera(user_camera)
        
        path = CameraScope + '/' + path_name
        target_prim = stage.GetPrimAtPath(path)
        camera_prim = stage.GetPrimAtPath(user_camera)
        camera_prim.GetAttribute('xformOp:translate').Set(target_prim.GetAttribute('xformOp:translate').Get())
        camera_prim.GetAttribute('xformOp:rotateYXZ').Set(target_prim.GetAttribute('xformOp:rotateYXZ').Get())
        
        return True