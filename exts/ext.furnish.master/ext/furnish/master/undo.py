import omni.usd

class ExtensionUndo():
    
    def __init__(self, controller) -> None:
        self.controller = controller
        self.Undo = []
        
        # [prims[], variants[], transform[]]
        self.lastUndo = []
        self.prims = []
        self.variants = []
        self.transform = []
        self.index = -1
    
    # =================================================================
    # Record 
    # =================================================================
    def saveUndo(self):
        if self.index != -1:
            temp = -1
            while temp != self.index:
                self.Undo.pop(temp)
                temp -= 1
            
        self.lastUndo = [self.prims, self.variants, self.transform]
        self.Undo.append(self.lastUndo)
        self.index = -1

        self.lastUndo = []
        self.prims = []
        self.variants = []
        self.transform = []
    
    def save_variant(self, prim, variantName):
        self.prims.append(prim)
        self.variants.append(variantName)
        self.transform.append(False)
    
    def save_transform(self, prim, trans):
        self.prims.append(prim)
        self.transform.append(trans)
        self.variants.append(False)
    
    # =================================================================
    # Action
    # =================================================================
    def undo(self):
        lastAction = self.Undo[self.index]
        prims = lastAction[0]
        variants = lastAction[1]
        transforms = lastAction[2]
        
        for i in range(len(prims)):
            if variants[i]:
                self.controller.variant_changed(prims[i], variants[i])
            
            if transforms[i]:
                self.controller.transform_changed(prims[i], transforms[i])
                
        if self.index-1 >= -len(self.Undo):
            self.index -= 1
        self.release_selection()
        self.controller.controller.selected_variant = []
        self.controller.controller.selected_variantPath = []
    
    def release_selection(self):
        ctx = omni.usd.get_context()
        ctx.get_selection().set_selected_prim_paths([], True)
        
    def shutdown(self):
        self.Undo = None
        self.lastUndo = None
        self.prims = None
        self.variants = None
        self.transform = None