

class ExtensionUndo():
    
    def __init__(self, controller) -> None:
        self.Undo = []
        
        # [prims[], variants[], transform[]]
        self.lastUndo = []
        self.prims = []
        self.variants = []
        self.transform = []
    
    # =================================================================
    # Record 
    # =================================================================
    def saveUndo(self):
        self.lastUndo = [self.prims, self.variants, self.transform]
        self.Undo.append(self.lastUndo)
        print(self.Undo)
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
    # Undo 
        
        
    def shutdown(self):
        self.Undo = None
        self.lastUndo = None
        self.prims = None
        self.variants = None
        self.transform = None