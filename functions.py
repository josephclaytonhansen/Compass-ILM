import bpy, pickle, json

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
        test_value = "EyeLoop" #get zone from sidebar panel
        if test_value not in self.ilm_atlas:
            v = CreateILMCBlank(self, test_value, 0)
            self.ilm_atlas[test_value] = {0:v}
    
g = Globals()
g.populate()
print(g.ilm_atlas)

def SaveUVData():
    g.uv_layer0.foreach_get("uv", g.uv_data0)
    g.uv_layer1.foreach_get("uv", g.uv_data1)
    g.uv_layer2.foreach_get("uv", g.uv_data2)


def UVDataTransfer():
    g.uv_layer0.foreach_set("uv", g.uv_data1)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')

