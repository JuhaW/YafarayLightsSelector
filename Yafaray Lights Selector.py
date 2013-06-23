bl_info = {
    "name": "Yafaray Lights Selector",
    "author": "TynkaTopi",
    "version": (1, 0),
    "blender": (2, 67, 0),
    "location": "Properties > Object",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}


import bpy

from bpy.props import BoolProperty
from bpy.props import IntProperty


# add your custom property to the Scene tpye

#Light counters

bpy.types.Scene.YafaL = IntProperty(default=0)
bpy.types.Scene.YafaMeshL = IntProperty(default=0)
bpy.types.Scene.YafaBGPortalL = IntProperty(default=0)
#checkboxes
bpy.types.Scene.bYafaL = BoolProperty(default=True)
bpy.types.Scene.bYafaMeshL = BoolProperty(default=True)
bpy.types.Scene.bYafaBGPortalL = BoolProperty(default=True)
#Render restricts
bpy.types.Scene.bYafaRendL = BoolProperty(default=True)
bpy.types.Scene.bYafaRendML = BoolProperty(default=True)
bpy.types.Scene.bYafaRendBGML = BoolProperty(default=True)


#--------------------
def UnselectObjects():
#--------------------
    #unselect all objects
    #bpy.ops.object.select_all(action = 'SELECT')
    bpy.ops.object.select_all(action='DESELECT')
    #bpy.context.scene.objects.active.select = False
    return{'Objects unselected'}
#--------------------


def Search_Lights():
#--------------------
    scene = bpy.context.scene
    scene.YafaL = 0
    scene.YafaMeshL = 0
    scene.YafaBGPortalL = 0

    #LAMPS
    for obj in bpy.context.scene.objects:
        if obj.type == 'LAMP':
            scene.YafaL = scene.YafaL + 1
            if scene.bYafaL is True:
                obj.select = True
            if scene.bYafaRendL is False:
                obj.hide_render = True
            else:
                obj.hide_render = False

    #print ("Lamps:",scene.YafaL)
    for obj in bpy.context.scene.objects:
        scene = bpy.context.scene
        if (obj.type == 'MESH'):

            #MESHLIGHTS
            if (obj.ml_enable is True):
                scene.YafaMeshL = scene.YafaMeshL + 1
                #print ('Meshlight:', obj.name)
                if scene.bYafaMeshL is True:
                    obj.select = True
                if scene.bYafaRendML is False:
                    obj.hide_render = True
                else:
                    obj.hide_render = False
            #BG MESHLIGHTS
            if (obj.bgp_enable is True):
                scene.YafaBGPortalL = scene.YafaBGPortalL + 1
                #print ('BG portal light:', obj.name)
                if scene.bYafaBGPortalL is True:
                    obj.select = True
                if scene.bYafaRendBGML is False:
                    obj.hide_render = True
                else:
                    obj.hide_render = False
    return{'FINISHED'}
#-----------------------------------------------


class YafarayLightsPanel(bpy.types.Panel):


    """Creates a Panel in the Object properties window"""

    bl_label = "YafaRay Lights Selector"
    bl_idname = "OBJECT_PT_hallo"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):


        layout = self.layout
        #obj = context.object
        scene = context.scene

        row = layout.row(align=True)
        # Create two columns, by using a split layout.
        split = layout.split(0.5)
        # First column

        col = split.column(align=True)

        col.label(text="Light Type")

        col.label(text= str(scene.YafaL) + " " + "Lamps",
             icon='OUTLINER_OB_LAMP')

        col.label(text= str(scene.YafaMeshL) + " " + "Mesh Lights",
             icon='LAMP_POINT')

        col.label(text= str(scene.YafaBGPortalL) + " " + "BG Portal Lights",
             icon='LAMP_AREA')

         # Second column, aligned
        col = split.column(align=True)
        # draw the checkbox (implied from property type = bool)

        col. label(text="Select")

        col.prop(scene, "bYafaL", "Lamps")
        col.prop(scene, "bYafaMeshL", "MeshL",)           
        col.prop(scene, "bYafaBGPortalL", "BGPortal")

        col = split.column(align=True)
        col. label(text="Render")
        col.prop(scene, "bYafaRendL", "", toggle=True, icon='RENDER_STILL',
             icon_only=True)
        col.prop(scene, "bYafaRendML", "", toggle=True, icon='RENDER_STILL',
             icon_only=True)
        col.prop(scene, "bYafaRendBGML", "", toggle=True, icon='RENDER_STILL',
             icon_only=True)

        #Search button
        #layout.separator()
        row = layout.row()
        row.operator("object.button", "Search/Select lights")



class OBJECT_OT_Button(bpy.types.Operator):
    """Search and select Lamps, Meshlights and BG Portal lights"""

    bl_idname = "object.button"
    bl_label = "Button"

    def execute(self, context):

        #print("Hello world!")
        UnselectObjects()
        Search_Lights()

        return{'FINISHED'}
#-----------------


def register():
    bpy.utils.register_class(YafarayLightsPanel)
    bpy.utils.register_class(OBJECT_OT_Button)


def unregister():
    bpy.utils.unregister_class(YafarayLightsPanel)
    bpy.utils.unregister_class(OBJECT_OT_Button)

if __name__ == "__main__":
    register()



#---------------------------------