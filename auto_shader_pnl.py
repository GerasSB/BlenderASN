bl_info = {
    "name": "Auto Shader Nodes",
    "author": "Geras",
    "version": (1, 3),
    "blender": (3, 5),
    "category": "Node",
    "location": "3DView",
    "description": "QoL features to help with Double Dash track creation",
    "warning": "",
    "doc_rul": "",
    "tracker_url": "",
}


import bpy
import os
import bmesh

#--Operators--

#Button 1
def alpha_shader(context):
    #This entire IF statement creates a shader group on the Blend file and puts everything inside it. Doesn't actually put
    #the shader group inside the material
    if bpy.data.node_groups.find('TransparencyGroup') == -1: #Checks if the blend file already has the group
        alphaGroup = bpy.data.node_groups.new('TransparencyGroup', 'ShaderNodeTree') #Creates the group
        
        #Create Transparent Shader inside group and move it
        alphatransparent = alphaGroup.nodes.new('ShaderNodeBsdfTransparent')
        alphatransparent.location = (-200,200)
        
        #Create Mix Shader inside group and move it
        alphaMixShader = alphaGroup.nodes.new('ShaderNodeMixShader')
        alphaMixShader.location = (0,0)
        
        #Create PrincipledBSDF Shader, set Specular value to 0 and move it
        alphaBsdf = alphaGroup.nodes.new('ShaderNodeBsdfPrincipled')
        alphaBsdf.location = (-500,0)
        alphaBsdf.inputs[7].default_value = 0
        
        #Create Material Output and move it
        alphaMatOutput = alphaGroup.nodes.new('ShaderNodeOutputMaterial')
        alphaMatOutput.location = (200,0)

        #Create Node Input and move it
        alphaInput = alphaGroup.nodes.new('NodeGroupInput')
        alphaInput.location = (-700, 0)
        
        #Creates sockets for the group inputs
        alphaGroup.inputs.new('NodeSocketFloatFactor', 'Alpha')
        alphaGroup.inputs.new('NodeSocketColor', 'Color')
        
        #Links all nodes together
        alphaGroup.links.new(alphaBsdf.outputs[0], alphaMixShader.inputs[2])
        alphaGroup.links.new(alphatransparent.outputs[0], alphaMixShader.inputs[1])
        alphaGroup.links.new(alphaMixShader.outputs[0], alphaMatOutput.inputs[0])
        alphaGroup.links.new(alphaInput.outputs[1], alphaBsdf.inputs[0])
        alphaGroup.links.new(alphaInput.outputs[0], alphaMixShader.inputs[0])


    #Creating the node inside the material
    sO = bpy.context.selected_objects
    for loopy in sO:
        currentmat = loopy.active_material.node_tree.nodes
        if currentmat.find('Image Texture') > -1:
            if currentmat.find('Principled BSDF') > -1 and currentmat.find('Material Output') > -1:
                #Find and remove Principled BSDF and Material Output nodes
                currentmatdelBSDF = currentmat.get('Principled BSDF')
                currentmat.remove(currentmatdelBSDF)
                currentmatdelOutput = currentmat.get('Material Output')
                currentmat.remove(currentmatdelOutput)
            
            #Creates Group Node inside material if there is none
            if currentmat.find('AlphaNode') == -1 and currentmat.find('Image Texture') > -1:
                newNodeGroup = currentmat.new('ShaderNodeGroup')#Add empty Node Group to material
                newNodeGroup.node_tree = bpy.data.node_groups['TransparencyGroup']#Convert empty Node Group to the TransparencyGroup
                loopy.active_material.node_tree.nodes["Group"].name = "AlphaNode" #Change the Node Group's name

            for noderinno in currentmat:
                if noderinno != currentmat.get('AlphaNode') and noderinno != currentmat.get('Image Texture'):
                    currentmat.remove(noderinno)

            #Link texture to nodes
            linkin = loopy.active_material.node_tree.links
            alphaGrpNode = currentmat.get('AlphaNode')
            getTex = currentmat.get('Image Texture')
            linkin.new(getTex.outputs[0], alphaGrpNode.inputs[1]) #Links color to group node
            linkin.new(getTex.outputs[1], alphaGrpNode.inputs[0]) #Links alpha to group node
                
            loopy.active_material.blend_method = 'HASHED' #Sets material blend method to Alpha Hashed
            
class AlphaShader(bpy.types.Operator):
    """Give selected meshes the Alpha shader group. Selected mesh needs an image
texture for this to work"""
    bl_idname = "shdr.alpha"
    bl_label = "Alpha Shader Group"
    
    def execute(self,context):
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            alpha_shader(context)
            return{'FINISHED'}

#Button 2
def vertex_shader(context):
    #This IF statement creates a shader group on the Blend file and puts everything inside it. Doesn't actually put
    #the shader group inside the material
    if bpy.data.node_groups.find('VertexGroup') == -1: #Checks if the blend file already has the group
        vertexGroup = bpy.data.node_groups.new('VertexGroup', 'ShaderNodeTree') #Creates the group
        create_vertex_group(vertexGroup, context)
        
def vertex_alpha_shader(context):
    #This entire IF statement creates a shader group on the Blend file and puts everything inside it. Doesn't actually put
    #the shader group inside the material
    if bpy.data.node_groups.find('VertexTGroup') == -1: #Checks if the blend file already has the group
        vertexGroup = bpy.data.node_groups.new('VertexTGroup', 'ShaderNodeTree') #Creates the group
        vertexVCnode, vertexBsdf = create_vertex_group(vertexGroup, context)
        vertexGroup.links.new(vertexVCnode.outputs[1], vertexBsdf.inputs[21])
        
        
def create_vertex_group(vertexGroup, context):        
    #Create Transparent Shader inside group and move it
    vertextransparent = vertexGroup.nodes.new('ShaderNodeBsdfTransparent')
    vertextransparent.location = (-200,200)
    
    #Create Mix Shader inside group and move it
    vertexMixShader = vertexGroup.nodes.new('ShaderNodeMixShader')
    vertexMixShader.location = (0,0)
    
    #Create PrincipledBSDF Shader and move it
    vertexBsdf = vertexGroup.nodes.new('ShaderNodeBsdfPrincipled')
    vertexBsdf.location = (-500,0)
    vertexBsdf.inputs[7].default_value = 0
    
    #Create Material Output and move it
    vertexMatOutput = vertexGroup.nodes.new('ShaderNodeOutputMaterial')
    vertexMatOutput.location = (200,0)

    #Create Node Input and move it
    vertexInput = vertexGroup.nodes.new('NodeGroupInput')
    vertexInput.location = (-700,0)
    
    #Creates sockets for the group inputs
    vertexGroup.inputs.new('NodeSocketFloatFactor', 'Alpha')
    vertexGroup.inputs.new('NodeSocketColor', 'Color')
    
    vertexVCnode = vertexGroup.nodes.new('ShaderNodeVertexColor')
    vertexVCnode.location = (-700,-200)
    
    vertexMixRGB = vertexGroup.nodes.new('ShaderNodeMixRGB')
    vertexMixRGB.location = (-600,0)
    vertexMixRGB.inputs[0].default_value = 0.98
    vertexMixRGB.blend_type = 'MULTIPLY'
    
    
    #Links all nodes together
    vertexGroup.links.new(vertexBsdf.outputs[0], vertexMixShader.inputs[2])
    vertexGroup.links.new(vertextransparent.outputs[0], vertexMixShader.inputs[1])
    vertexGroup.links.new(vertexMixShader.outputs[0], vertexMatOutput.inputs[0])
    vertexGroup.links.new(vertexInput.outputs[1], vertexMixRGB.inputs[1])
    vertexGroup.links.new(vertexInput.outputs[0], vertexMixShader.inputs[0])
    vertexGroup.links.new(vertexVCnode.outputs[0], vertexMixRGB.inputs[2])
    vertexGroup.links.new(vertexMixRGB.outputs[0], vertexBsdf.inputs[0])
    return vertexVCnode, vertexBsdf

def link_vertex_nodes(groupName, nodeName, blendmode, context):
    #Creating the node group inside the material
    sO = bpy.context.selected_objects
    for loopy in sO:
        currentmat = loopy.active_material.node_tree.nodes
        getObjName = loopy.data.name
        vColorAmount = bpy.data.meshes[getObjName].vertex_colors.items() #Checks if material has vertex colors
        if vColorAmount != [] and currentmat.find('Image Texture') > -1: #If object has vertex colors and image textures...
            if currentmat.find('Principled BSDF') > -1 and currentmat.find('Material Output') > -1 and currentmat.find('Image Texture') > -1:
                #Find and remove Principled BSDF and Material Output nodes
                currentmatdelBSDF = currentmat.get('Principled BSDF')
                currentmat.remove(currentmatdelBSDF)
                currentmatdelOutput = currentmat.get('Material Output')
                currentmat.remove(currentmatdelOutput)
            
            #Creates Group Node inside material if there is none
            if currentmat.find(nodeName) == -1:
                newNodeGroup = currentmat.new('ShaderNodeGroup') #Add empty Node Group to material
                newNodeGroup.node_tree = bpy.data.node_groups[groupName] #Convert empty Node Group to the VertexGroup
                loopy.active_material.node_tree.nodes["Group"].name = nodeName
            
            linkin = loopy.active_material.node_tree.links #Create link reference
            alphaGrpNode = currentmat.get(nodeName)
            #Linking the texture to the node
            for noderinno in currentmat:
                if (noderinno != currentmat.get('Image Texture')) and (noderinno !=currentmat.get(nodeName)):
                    currentmat.remove(noderinno)
            #if currentmat.find('Image Texture') > -1:
                #if currentmat.find('AlphaNode') > -1:
                    #delAnode = currentmat.get('AlphaNode')
                    #currentmat.remove(delAnode)
                    
            getTex = currentmat.get('Image Texture') #Creates a variable for the Texture node
            linkin.new(getTex.outputs[0], alphaGrpNode.inputs[1]) #Links color to group node
            linkin.new(getTex.outputs[1], alphaGrpNode.inputs[0]) #Links alpha to group node
            
            loopy.active_material.blend_method = blendmode #Sets material blend method to Alpha Hashed
            
class VertexShader(bpy.types.Operator):
    """Give selected meshes the Vertex shader group. Selected mesh needs to have
vertex colors AND image textures for this button to work"""
    bl_idname = "shdr.vertex"
    bl_label = "Vertex Shader Group"
    
    def execute(self,context):
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            vertex_shader(context)
            link_vertex_nodes('VertexGroup','VertexNode', 'HASHED', context)
            return{'FINISHED'}

class VertexTransparencyShader(bpy.types.Operator):
    """Give selected meshes the Vertex Transparency shader group. It allows to
see transparency in vertex data. Selected mesh needs vertex colors AND image
textures for this button to work"""
    bl_idname = "shdr.vertextrans"
    bl_label = "Vertex Transparency Group"
    
    def execute(self,context):
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            vertex_alpha_shader(context)
            link_vertex_nodes('VertexTGroup','VertexTNode', 'HASHED', context)
            return{'FINISHED'}

#Button 3 - Remove groups
def remove_groups(context):
    
    #Creating the node inside the material
    sO = bpy.context.selected_objects
    for loopy in sO:
        currentmat = loopy.active_material.node_tree.nodes
        
        # Cycle through all nodes and delete them (except for Image Texture nodes)
        if currentmat.find('Image Texture') != -1:
            for noderinno in currentmat:
                if noderinno != currentmat.get('Image Texture'):
                    currentmat.remove(noderinno)
                    
            #Create Principled BSDF
            expbsdf = currentmat.new('ShaderNodeBsdfPrincipled')
            expbsdf.location = (200, 0)
            expbsdf.inputs[7].default_value = 0
            
            #Create Output Material
            exout = currentmat.new('ShaderNodeOutputMaterial')
            exout.location = (500, 0)
            
            #Linking the texture to the nodes
            linkin = loopy.active_material.node_tree.links #Create link reference
            
            getTex = currentmat.get('Image Texture') #Creates a variable for the Texture node
            linkin.new(getTex.outputs[0], expbsdf.inputs[0]) #Links color to group node
            linkin.new(expbsdf.outputs[0], exout.inputs[0]) #Links alpha to group node

class ExportSelected(bpy.types.Operator):
    """Blender can't export materials with shader groups, so use this button
before exporting"""
    bl_idname = "shdr.export"
    bl_label = "Remove Groups (for export)"
    
    def execute(self,context):
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            remove_groups(context)
            return{'FINISHED'}
    
#Color Button       
def button_04(context):
    scn = bpy.context.scene
    scn.view_settings.exposure = 3.95
    scn.view_settings.gamma = 1

            
class ColorScene(bpy.types.Operator):
    """Change Exposure and Gamma settings to better match Double Dash's lighting,
for more accurate viewport previews in Eevee Render Mode"""
    bl_idname = "shdr.color"
    bl_label = "Change Exposure & Gamma"
    
    def execute(self,context):
        button_04(context)
        return{'FINISHED'}

# Export DAE Class   
class ExportDae(bpy.types.Operator):
    """Export all selected objects as DAE to a 'course' folder inside the Blender
file's current directory"""
    bl_idname = "shdr.exportdae"
    bl_label = "Export Selection as DAE"
    
    def execute(self,context):
        exclude(context)
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            export_checks(self, context, '.dae')
            return{'FINISHED'}

class ExportObj(bpy.types.Operator):
    """Export all selected objects as OBJ to a 'course_collision' folder inside
the Blender file's current directory"""
    bl_idname = "shdr.exportobj"
    bl_label = "Export Selection as OBJ"
    
    def execute(self,context):
        exclude(context)
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            export_checks(self, context, '.obj')
            return{'FINISHED'}

def dae_export(pathname, context):
        remove_groups(context)
        bpy.ops.wm.collada_export(filepath=pathname, selected=True, triangulate=True)

def obj_export(pathname, context):
        remove_groups(context)
        bpy.ops.wm.obj_export(filepath=pathname, export_selected_objects=True, export_triangulated_mesh=True, check_existing=False)

def set_pathname(self, context, type, course_name):
    pathname = bpy.context.blend_data.filepath
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    if type == '.dae':
        pathname = pathname.removesuffix(filename) + 'course\\'
        filename = course_name + '_course.dae'
        pathname = pathname + filename
        dae_export(pathname, context)
        self.report({'INFO'}, 'File exported to ' + pathname)
        
    elif type == '.obj':
        pathname = pathname.removesuffix(filename) + 'course_collision\\'
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        filename = course_name + '_course.obj'
        pathname = pathname + filename
        obj_export(pathname, context)
        self.report({'INFO'}, 'File exported to ' + pathname)
        
# Some checks before exporting DAE and returns the path it'll export to
def export_checks(self, context, type):
    course_name = context.scene.my_tool.course_name
    if bpy.context.blend_data.filepath != '':
        if bpy.context.selected_objects == []:
            self.report({'ERROR'}, 'Please select the objects to export and try again')
        elif course_name == '':
            self.report({'ERROR'}, "Please enter your course's name")
        else:
            set_pathname(self, context, type, course_name)
    else:
        self.report({'ERROR'}, 'Save your Blender project somewhere before exporting')

def exclude(context):
    for i in bpy.context.selected_objects:
        if 'EXCLUDE' in i.name:
            i.select_set(False)     
#--Panel--
from bpy.types import Panel

def check_selection(self, context):
    for i in bpy.context.selected_objects:
        if i.type != 'MESH':
            i.select_set(False)
            # self.report({'ERROR'}, "You're selecting a non-mesh object. Aborting.")
            # return {'CANCELLED'}
            continue
        elif i.active_material == None:
            self.report({'ERROR'}, "Mesh [" + i.name + "] doesn't have a material assigned. Aborting.")
            return {'CANCELLED'}

def roadtype_info(self, context):
    roadtypes = context.scene.my_tool.roadtypes
    context.scene.my_tool.roadinfo_falling = '-'
    context.scene.my_tool.roadinfo_index = '-'
    context.scene.my_tool.roadinfo_respawn = '-'
    try:
        material_slot = bpy.context.active_object.active_material.name
    except:
        self.report({'ERROR'}, 'No material selected')
        return {'CANCELLED'}
    else:
        for type in roadtypes:
            if type in material_slot:
                context.scene.my_tool.roadinfo = type.removeprefix('Roadtype_') + " = " + roadtypes[type]
                context.scene.my_tool.roadinfo_index = geosplash_index(context, type, material_slot)
                context.scene.my_tool.roadinfo_falling = falling_animation(context, type, material_slot)
                context.scene.my_tool.roadinfo_respawn = respawn_id(type, material_slot)
                return {'FINISHED'}
    self.report({'ERROR'}, 'No collision has the name ' + "'" + material_slot + "'")
    context.scene.my_tool.roadinfo = 'Not a valid collision name'
    return {'FINISHED'}

def falling_animation(context, type, material_name):
    VALID_MAT_LENGTH = context.scene.my_tool.VALID_MAT_LENGTH
    VALID_DEADZONES = ['0x0F', '0x0A']
    falling_id = material_name[-3]
    animation_type = ''
    if len(material_name) in VALID_MAT_LENGTH and type.removeprefix('Roadtype_') in VALID_DEADZONES:
        if falling_id == '1':
            animation_type = "Falling animation enabled"
        elif falling_id == '0':
            animation_type = "Falling animation disabled"
        else:
            animation_type = "Invalid falling animation ID"
        return animation_type
    else:
        return '-'

def geosplash_index(context, type, material_name):
    VALID_MAT_LENGTH = context.scene.my_tool.VALID_MAT_LENGTH
    if type.removeprefix('Roadtype_') == '0x0F':
        if len(material_name) in VALID_MAT_LENGTH:
            index = 'GeoSplash Index = ' + str(material_name[-1])
            return index
        else:
            return '!!! MISSING INDEX !!!'
    else:
        return '-'

def respawn_id(type, material_name):
    VALID_RESPAWN = ['0x05', '0x07', '0x09', '0x0A', '0x0B', '0x0D', '0x0E', '0x0F', '0x10', '0x11', '0x37', '0x47']
    if type.removeprefix('Roadtype_') in VALID_RESPAWN:
        if material_name[13] == '0':
            respawnid = str(material_name[14])
        else:
            respawnid = str(material_name[13:15])
        respawnid = 'Respawn ID = ' + respawnid
        return respawnid
    else:
        return '-'
        

class P1_PT_AutoShaderNodes(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Auto Shader Nodes"
    bl_category = "ASN"
    
    def draw(self, context):
        
        #Alpha Button
        self.layout.operator("shdr.alpha")
        
        #Vertex Button
        self.layout.operator("shdr.vertex")
        
        #Vertex Transparency Button
        self.layout.operator("shdr.vertextrans")
        
        #Remove Button
        self.layout.operator("shdr.export")
        
class P2_PT_ViewportSettings(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Viewport Settings"
    bl_category = "ASN"
    
    def draw(self, context):
        
        #Alpha Button
        self.layout.operator("shdr.color")

def select_vertical_geometry(self, context):
    if bpy.context.selected_objects == []:
        self.report({'ERROR'}, "Please select a mesh")
        return {'CANCELLED'}
    strength = context.scene.my_tool.vertical_strength * 0.24
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cylinder_add(vertices=200, end_fill_type='NOTHING', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    # Create a bmesh access
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    bm.faces.ensure_lookup_table()

    # Get faces access
    bm.faces.ensure_lookup_table()
    selected_faces = [face for face in bm.faces if face.select]
            
    bpy.ops.mesh.select_similar(type='NORMAL', threshold=strength)
    
    # Delete everything on the selected_faces variable
    bmesh.ops.delete(bm, geom =selected_faces, context='FACES')
    
class SelectVerticalGeometry(bpy.types.Operator):
    """Selects all* vertical geometry from the selected object(s).
    
* Adjust the strength to taste (the lower the number, the steeper the polygon).
The default of 0.50 is recommended as walls won't get steeper than that, though
roads can go as steep as 0.38"""
    bl_idname = "shdr.removevertical"
    bl_label = "Select Vertical Geometry"
    
    def execute(self, context):
        result = check_selection(self, context)
        if result == {'CANCELLED'}:
            return {'CANCELLED'}
        else:
            select_vertical_geometry(self, context)
            return{'FINISHED'}
    
class RoadtypeInfo(bpy.types.Operator):
    """Tells you the type of collision of your currently active material"""
    bl_idname = "shdr.roadtypeinfo"
    bl_label = "Roadtype Info"
    
    def execute(self, context):
        roadtype_info(self, context)
        return{'FINISHED'}
    

# Export Panel
class P3_PT_Export(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Export"
    bl_category = "ASN"
    
    def draw(self, context):
        
        my_tool = context.scene.my_tool
        
        
        #Operators
        
        #Course name
        row = self.layout.row()
        row.label(text = 'Course Name')
        self.layout.prop(my_tool, 'course_name')
        self.layout.separator()
        
        #Export button
        self.layout.operator("shdr.exportdae")
        self.layout.operator("shdr.exportobj")

# Tools Panel
class P4_PT_CollisionTools(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Collision Tools"
    bl_category = "ASN"
    
    def draw(self, context):
        my_tool = context.scene.my_tool
        
        self.layout.operator("shdr.removevertical")
        self.layout.prop(my_tool, 'vertical_strength')
        self.layout.separator()
        self.layout.operator("shdr.roadtypeinfo")
        self.layout.label(text=my_tool.roadinfo)
        self.layout.label(text=my_tool.roadinfo_respawn)
        self.layout.label(text=my_tool.roadinfo_falling)
        self.layout.label(text=my_tool.roadinfo_index)
        
class MyProperties(bpy.types.PropertyGroup):
    
    course_name : bpy.props.StringProperty(name='',
        description="Only enter the course's unique identifier, WITHOUT _course. Example: luigi",
        default="")
        
    vertical_strength : bpy.props.FloatProperty(name='Strength', soft_min=0.37, soft_max=1, default=0.50, min=0, max=1)
    
    roadinfo : bpy.props.StringProperty(name='')
    roadinfo_respawn : bpy.props.StringProperty(name='-')
    roadinfo_index : bpy.props.StringProperty(name='-')
    roadinfo_falling : bpy.props.StringProperty(name='-')

    roadtypes = {
        "Roadtype_0x00": "Medium offroad, mud",
        "Roadtype_0x01": "Normal road",
        "Roadtype_0x02": "Kart and item wall",
        "Roadtype_0x03": "Medium offroad, grass",
        "Roadtype_0x04": "Slippery ice road",
        "Roadtype_0x05": "Road-level deadzone",
        "Roadtype_0x06": "???",
        "Roadtype_0x07": "Ramp boost",
        "Roadtype_0x08": "Boost",
        "Roadtype_0x09": "Cannon",
        "Roadtype_0x0A": "Aerial deadzone",
        "Roadtype_0x0B": "Sand road",
        "Roadtype_0x0C": "Weak sand offroad",
        "Roadtype_0x0D": "Pipe teleportation",
        "Roadtype_0x0E": "Sand deadzone",
        "Roadtype_0x0F": "Water/lava deadzone",
        "Roadtype_0x10": "Quicksand sinkhole",
        "Roadtype_0x11": "Sand deadzone w/ water",
        "Roadtype_0x12": "Kart-exclusive wall",
        "Roadtype_0x13": "Heavy offroad",
        "Roadtype_0x37": "Ramp boost for gaps",
        "Roadtype_0x47": "Ramp boost for gaps"
    }

    VALID_MAT_LENGTH = [26, 31]



#--Blender stuff--        
def register():
    bpy.utils.register_class(P1_PT_AutoShaderNodes)
    bpy.utils.register_class(AlphaShader)
    bpy.utils.register_class(VertexShader)
    bpy.utils.register_class(VertexTransparencyShader)
    bpy.utils.register_class(ExportSelected)
    bpy.utils.register_class(P2_PT_ViewportSettings)
    bpy.utils.register_class(P3_PT_Export)
    bpy.utils.register_class(P4_PT_CollisionTools)
    bpy.utils.register_class(ColorScene)
    bpy.utils.register_class(ExportDae)
    bpy.utils.register_class(ExportObj)
    bpy.utils.register_class(SelectVerticalGeometry)
    bpy.utils.register_class(RoadtypeInfo)
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)

def unregister():
    bpy.utils.unregister_class(P1_PT_AutoShaderNodes)
    bpy.utils.unregister_class(AlphaShader)
    bpy.utils.unregister_class(VertexShader)
    bpy.utils.unregister_class(VertexTransparencyShader)
    bpy.utils.unregister_class(ExportSelected)
    bpy.utils.unregister_class(P2_PT_ViewportSettings)
    bpy.utils.unregister_class(P3_PT_Export)
    bpy.utils.unregister_class(P4_PT_CollisionTools)
    bpy.utils.unregister_class(ColorScene)
    bpy.utils.unregister_class(ExportDae)
    bpy.utils.unregister_class(RoadtypeInfo)
    bpy.utils.unregister_class(SelectVerticalGeometry)
    bpy.utils.unregister_class(ExportObj)
    bpy.utils.unregister_class(MyProperties)
    del bpy.types.Scene.my_tool
    
if __name__ == "__main__":
        register()