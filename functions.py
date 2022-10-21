import bpy, pickle, json
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,)
                       
                       
### Functions ###
                       
def CreateILMCBlank(g, zone, index):
    filename = zone+"_block"+str(index)+".ilmc"
    with open(g.project_dir+filename, "w") as f:
        pass
    return filename
        

class Globals:
    me = bpy.context.object.data
    num_loops = len(me.loops)
    uv_layer0 = me.uv_layers[0].data
    uv_layer1 = me.uv_layers[1].data
    uv_layer2 = me.uv_layers[2].data
    uv_data0 = [0] * num_loops * 2  # Loops times uv dimensions
    uv_data1 = [0] * num_loops * 2
    uv_data2 = [0] * num_loops * 2
    project_dir = "H:\\blender\\projects\\pmh\\" #get from sidebar
    
    ilm_atlas = {}
    #populate with zones
    
    def populate(self):
        zone_name = bpy.data.scenes["Scene"].zone_name
        if zone_name not in self.ilm_atlas:
            v = CreateILMCBlank(self, zone_name, 0)
            self.ilm_atlas[zone_name] = {0:v}
    
g = Globals()


def SaveUVData():
    g.uv_layer0.foreach_get("uv", g.uv_data0)
    g.uv_layer1.foreach_get("uv", g.uv_data1)
    g.uv_layer2.foreach_get("uv", g.uv_data2)


def UVDataTransfer():
    g.uv_layer0.foreach_set("uv", g.uv_data1)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')


### Operators ###

class AddZone(Operator):
    """Add UV zone"""
    bl_idname = "wm.add_zone"
    bl_label = "Add zone"
    def execute(self,context):
        g.populate()
        return {'FINISHED'}


### Draw ###

bl_info = {
    'name': 'Compass ILM',
    'category': 'Animation',
    'author': 'Joseph Hansen',
    'version': (1, 0, 0),
    'blender': (3, 3, 0),
    'location': '',
    'description': ''
}


class OBJECT_PT_CompassPanel(Panel):
    bl_label = "Compass ILM"
    bl_idname = "OBJECT_PT_compass_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Animation"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        #prop, operator, label
        
        subrow = layout.row(align=True)
        
        subrow.prop(scene, "zone_name")
        subrow.operator("wm.add_zone")

classes = [OBJECT_PT_CompassPanel, AddZone]


### Register / unregister ###

def register():
    for c in classes: bpy.utils.register_class(c)
    bpy.types.Scene.zone_name = StringProperty(name = "Zone")

def unregister():
    for c in classes: bpy.utils.unregister_class(c)
    for i in [bpy.types.Scene.zone_name]:
        del i


if __name__ == "__main__":
    register()