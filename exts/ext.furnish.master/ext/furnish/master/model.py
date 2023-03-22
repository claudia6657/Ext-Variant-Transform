import omni.usd
from pxr import Gf
from .undo import ExtensionUndo
class ExtensionModel():

    def __init__(self, controller):
        self.controller = controller
        self.chairVariantList = []
        self.computorVariantList = []
        self.machineVariantList = []
        self.chairPath = []
        self.computerPath = []
        self.machinePath = []
        self.get_all_variant_prim()
        # chair, computer, machine
        self.transform = []
        self.transform.append(self.Get_VariantItem_transform(self.chairPath[-1]))
        self.transform.append(self.Get_VariantItem_transform(self.computerPath[-1]))
        self.transform.append(self.Get_VariantItem_transform(self.machinePath[-1]))
        self.newChairTransform = None
        self.newMachineTransform = None
        self.newComputerTransform = None
        self.newTransform = [self.newChairTransform, self.newComputerTransform, self.newMachineTransform]
        
        self.machine_variant_names = self.Get_Variant_Names(self.machineVariantList[0])
        self.chair_variant_names = self.Get_Variant_Names(self.chairVariantList[0])
        self.computer_variant_names = self.Get_Variant_Names(self.computorVariantList[0])
        self.undo = ExtensionUndo(self)
    
    # DEFAULT CATEGORY
    def variantCategory(self, prim):
        name = prim.GetName()
        path = str(prim.GetPath()).split('/OmniVariants')[0]
        if 'Chair' in name:
            self.chairVariantList.append(prim)
            self.chairPath.append(path)
        elif 'Computer' in name:
            self.computorVariantList.append(prim)
            self.computerPath.append(path)
        elif 'Machine' in name and prim not in self.machineVariantList:
            self.machineVariantList.append(prim)
            self.machinePath.append(path)
        
    def get_all_variant_prim(self):
        def find_desandant(prim):
            primpath = prim.GetName()
            if 'OmniVariants' in primpath:
                self.variantCategory(prim)
                return True
            if prim.GetChildren():
                for child in prim.GetChildren():
                    desandant = find_desandant(child)
                    if desandant:
                        pass
                return True
        
        basePath = '/World'
        stage = omni.usd.get_context().get_stage()
        basePrim = stage.GetPrimAtPath(basePath)
        
        for i in basePrim.GetChildren():
            variant = find_desandant(i)
    
    def get_variant_selection(self, variant_item):
        variantprim = self.check_variant_prim(variant_item)
        if variantprim:
            variant = variantprim.GetVariantSets().GetVariantSet("modelingVariant")
            selection = variant.GetVariantSelection()
            return selection
        return 0
    
    def Get_Variant_Names(self, variantprim):
        variant = variantprim.GetVariantSets().GetVariantSet("modelingVariant").GetVariantNames()        
        return variant
    
    def Get_VariantItem_transform(self, path):
        trans = []
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(path)
        
        trans.append(prim.GetAttribute('xformOp:translate').Get())
        trans.append(prim.GetAttribute('xformOp:rotateXYZ').Get())
        trans.append(prim.GetAttribute('xformOp:scale').Get())
        return trans
    
    # Variants Command
    def variant_changed(self, variant_item, variant_name):
        if variant_item == None:
            return 0

                 
        variant = variant_item.GetVariantSets().GetVariantSet("modelingVariant")
        name = variant.GetVariantNames()
        if variant_name not in name:
            return 0
        
        old_variant_name = variant.GetVariantSelection()
        self.undo.save_variant(variant_item, old_variant_name)
        variant.SetVariantSelection(variant_name)        
        
        """ REFLOW MODEL ISSUE """
        stage = omni.usd.get_context().get_stage()         

        path = str(variant_item.GetPath()).split('/OmniVariants')[0]
        prim = stage.GetPrimAtPath(path)
        if variant_name == 'Reflow':
            temp = [
                prim.GetAttribute('xformOp:translate').Get(),
                prim.GetAttribute('xformOp:rotateXYZ').Get()+Gf.Vec3d(0, 90, 0),
                prim.GetAttribute('xformOp:scale').Get()
            ]
            self.transform_changed(prim, temp)
        if old_variant_name == 'Reflow':
            temp = [
                prim.GetAttribute('xformOp:translate').Get(),
                prim.GetAttribute('xformOp:rotateXYZ').Get()-Gf.Vec3d(0, 90, 0),
                prim.GetAttribute('xformOp:scale').Get()
            ]
            self.transform_changed(prim, temp)
        return 1
    
    def transform_changed(self, prim, trans):
        prim.GetAttribute('xformOp:translate').Set(trans[0])
        prim.GetAttribute('xformOp:rotateXYZ').Set(trans[1])
        prim.GetAttribute('xformOp:scale').Set(trans[2])
        return 1
    
    # Set ALL
    def allchair_variants_changed(self, variant_name):
        for i in self.chairVariantList:
            self.variant_changed(i, variant_name)

    def allcomputer_variants_changed(self, variant_name):
        for i in self.computorVariantList:
            self.variant_changed(i, variant_name)
            
    def allmachine_variants_changed(self, variant_name):
        print('start loop')
        for i in self.machineVariantList:
            self.variant_changed(i, variant_name)
    
    def all_transform_changed(self):
        self.PL = ['/World/PL_01', '/World/PL_02', '/World/PL_03', '/World/PL_04']
        trans_item = [self.chairPath, self.computerPath, self.machinePath]
        new_transform = []
        ''' If any item transform changed '''
        for i in range(len(self.newTransform)):
            if self.newTransform[i]:
                temp = self.Get_VariantItem_transform(self.newTransform[i])
                new_transform.append(temp)
            else:
                new_transform.append(self.transform[i])
        
        for i in range(0, len(new_transform)):
            if new_transform[i] != self.transform[i]:
                for path in trans_item[i]:
                    if self.newTransform[i] in path:
                        pass
                    else:
                        stage = omni.usd.get_context().get_stage()
                        prim = stage.GetPrimAtPath(path)
                        # translate= prim.GetAttribute('xformOp:translate').Get()
                        rotate = prim.GetAttribute('xformOp:rotateXYZ').Get()
                        prim.GetAttribute('xformOp:translate').Set(new_transform[i][0])
                        if self.controller._menu_win.menu_value[2]:
                            prim.GetAttribute('xformOp:rotateXYZ').Set(rotate+(new_transform[i][1]-self.transform[i][1]))
                        prim.GetAttribute('xformOp:scale').Set(new_transform[i][2])     
        
                        self.undo.save_transform(prim, self.transform[i])

    def check_variant_prim(self, variant_item):
        stage = omni.usd.get_context().get_stage()
        if variant_item == None:
            prim = None
        elif variant_item == 'chair':
            prim = self.chairVariantList[-1]
        elif variant_item == 'monitor' or variant_item == 'computer':
            prim = self.computorVariantList[-1]
        elif variant_item == 'machine':
            prim = self.machineVariantList[-1]
        else:
            prim = variant_item
            
        return prim

    def check_variant_path(self, variant_item):
        variant_item = variant_item.lower()
        if variant_item == None:
            path = None
        elif variant_item == 'chair':
            path = self.chairPath[-1]
        elif variant_item == 'monitor'or variant_item == 'computer':
            path = self.computerPath[-1]
        elif variant_item == 'machine':
            path = self.machinePath[-1]
        else:
            path = variant_item
            
        return path

    # SELECTION    
    def item_changed(self, category):
        item = self.check_variant_path(category)
        if item and self.controller.selected_variant == []:
            ctx = omni.usd.get_context()
            selection = ctx.get_selection().set_selected_prim_paths([item], True)
            self.controller.selected_variant.append(item)
        
    def shutdown(self):
        self.chairVariantList = None
        self.computorVariantList = None
        self.machineVariantList = None
        self.machine_variant_names = None
        self.chair_variant_names = None
        self.computer_variant_names = None
        self.chairPath = None
        self.computerPath = None
        self.machinePath = None
        self.transform  = None
        self.newTransform = None
