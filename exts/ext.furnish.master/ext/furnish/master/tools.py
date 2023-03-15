import omni.usd

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