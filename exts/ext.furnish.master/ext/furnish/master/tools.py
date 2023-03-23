import omni.usd
import omni.kit.commands
from omni.kit.viewport.utility import get_active_viewport

AreaCameraScope = '/World/ExtCamera/AreaCamera'
FloorCameraScope = '/World/ExtCamera/FloorCamera'
UserCamera = '/World/ExtCamera/User' 

class ExtensionTool():
    
    def __init__(self, controller) -> None:
        self.controller = controller
        self.user = self.Get_CAM(UserCamera)
        if not self.user:
            self.Build_CAMs(UserCamera)
            self.user = self.Get_CAM(UserCamera)
            
        self.area = self.Get_CAM(AreaCameraScope)
        if not self.area:
            self.Build_CAMs(AreaCameraScope)
            self.user = self.Get_CAM(AreaCameraScope)
    
        self.floor = self.Get_CAM(FloorCameraScope)
        if not self.floor:
            self.Build_CAMs(FloorCameraScope)
            self.user = self.Get_CAM(FloorCameraScope)
                        
    def Build_CAMs(self, path):
        omni.kit.commands.execute("CreatePrimCommand", prim_type='Camera', prim_path=path, attributes={'focusDistance': 400, 'focalLength': 24})
        return True
     
    def Build_Scope(self,path):
        omni.kit.commands.execute("CreatePrimCommand", prim_type='Scope', prim_path=path)
        return True
        
    def Get_CAM(self, path):
        stage = omni.usd.get_context().get_stage()
        Prim = stage.GetPrimAtPath(path)
        return Prim
        
    def Get_Area_Camera(self):
        stage = omni.usd.get_context().get_stage()
        basePrim = stage.GetPrimAtPath(AreaCameraScope)
        
        if not basePrim:
            return False
        for i in basePrim.GetChildren():
            self.controller.Area.append(i.GetName())
        
        return True

    def Get_Floor_Camera(self):
        stage = omni.usd.get_context().get_stage()
        basePrim = stage.GetPrimAtPath(FloorCameraScope)
        
        if not basePrim:
            return False
        for i in basePrim.GetChildren():
            self.controller.Floor.append(i.GetName())
        
        return True

    def Change_Active_Camera(self, camera_path):
        viewport = get_active_viewport()

        if not viewport:
            raise RuntimeError("No active Viewport")

        viewport.camera_path = camera_path
        
    def Load_Area_Position(self, path_name):
        stage = omni.usd.get_context().get_stage()

        user_camera = UserCamera
        self.Change_Active_Camera(user_camera)
        
        path = AreaCameraScope + '/' + path_name
        target_prim = stage.GetPrimAtPath(path)
        camera_prim = stage.GetPrimAtPath(user_camera)
        camera_prim.GetAttribute('xformOp:translate').Set(target_prim.GetAttribute('xformOp:translate').Get())
        camera_prim.GetAttribute('xformOp:rotateYXZ').Set(target_prim.GetAttribute('xformOp:rotateYXZ').Get())
        
        return True
    
    def Load_Floor_Position(self, path_name):
        stage = omni.usd.get_context().get_stage()

        user_camera = UserCamera
        self.Change_Active_Camera(user_camera)
        
        path = FloorCameraScope + '/' + path_name
        target_prim = stage.GetPrimAtPath(path)
        camera_prim = stage.GetPrimAtPath(user_camera)
        camera_prim.GetAttribute('xformOp:translate').Set(target_prim.GetAttribute('xformOp:translate').Get())
        camera_prim.GetAttribute('xformOp:rotateYXZ').Set(target_prim.GetAttribute('xformOp:rotateYXZ').Get())
        
        return True