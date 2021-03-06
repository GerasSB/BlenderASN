bl_info = {
    "name": "Auto Shader Nodes",
    "author": "Geras",
    "version": (1, 0),
    "blender": (3, 1),
    "category": "Node",
    "location": "3DView",
    "description": "QoL features to make previewing finished models easier",
    "warning": "",
    "doc_rul": "",
    "tracker_url": "",
}


import bpy

#--Operators--

#Button 1
def button_01(context):
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
        if currentmat.find('Principled BSDF') > -1 and currentmat.find('Material Output') > -1 and currentmat.find('Image Texture') > -1:
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
        
        linkin = loopy.active_material.node_tree.links #Create link reference
        alphaGrpNode = currentmat.get('AlphaNode')
        #Linking the texture to the node
        if currentmat.find('Image Texture') > -1:
            if currentmat.find('VertexNode') > -1:
                delVnode = currentmat.get('VertexNode')
                currentmat.remove(delVnode)
            getTex = currentmat.get('Image Texture') #Creates a variable for the Texture node
            linkin.new(getTex.outputs[0], alphaGrpNode.inputs[1]) #Links color to group node
            linkin.new(getTex.outputs[1], alphaGrpNode.inputs[0]) #Links alpha to group node
            
            loopy.active_material.blend_method = 'HASHED' #Sets material blend method to Alpha Hashed
            
class clssAlphaShader(bpy.types.Operator):
    """Give selected meshes the Alpha shader group. Use this one before you try the Vertex Nodes button."""
    bl_idname = "shdr.alpha"
    bl_label = "Alpha Shader Group"
    
    def execute(self,context):
        button_01(context)
        return{'FINISHED'}


#Button 2
def button_02(context):
    #This entire IF statement creates a shader group on the Blend file and puts everything inside it. Doesn't actually put
    #the shader group inside the material
    if bpy.data.node_groups.find('VertexGroup') == -1: #Checks if the blend file already has the group
        vertexGroup = bpy.data.node_groups.new('VertexGroup', 'ShaderNodeTree') #Creates the group
        
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
        vertexMixRGB.inputs[0].default_value = 1
        vertexMixRGB.blend_type = 'MULTIPLY'
        
        
        #Links all nodes together
        vertexGroup.links.new(vertexBsdf.outputs[0], vertexMixShader.inputs[2])
        vertexGroup.links.new(vertextransparent.outputs[0], vertexMixShader.inputs[1])
        vertexGroup.links.new(vertexMixShader.outputs[0], vertexMatOutput.inputs[0])
        vertexGroup.links.new(vertexInput.outputs[1], vertexMixRGB.inputs[1])
        vertexGroup.links.new(vertexInput.outputs[0], vertexMixShader.inputs[0])
        vertexGroup.links.new(vertexVCnode.outputs[0], vertexMixRGB.inputs[2])
        vertexGroup.links.new(vertexMixRGB.outputs[0], vertexBsdf.inputs[0])

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
            if currentmat.find('VertexNode') == -1:
                newNodeGroup = currentmat.new('ShaderNodeGroup')#Add empty Node Group to material
                newNodeGroup.node_tree = bpy.data.node_groups['VertexGroup']#Convert empty Node Group to the TransparencyGroup
                loopy.active_material.node_tree.nodes["Group"].name = "VertexNode"
            
            linkin = loopy.active_material.node_tree.links #Create link reference
            alphaGrpNode = currentmat.get('VertexNode')
            #Linking the texture to the node
            if currentmat.find('Image Texture') > -1:
                if currentmat.find('AlphaNode') > -1:
                    delAnode = currentmat.get('AlphaNode')
                    currentmat.remove(delAnode)
                getTex = currentmat.get('Image Texture') #Creates a variable for the Texture node
                linkin.new(getTex.outputs[0], alphaGrpNode.inputs[1]) #Links color to group node
                linkin.new(getTex.outputs[1], alphaGrpNode.inputs[0]) #Links alpha to group node
                
                loopy.active_material.blend_method = 'HASHED' #Sets material blend method to Alpha Hashed
            
class clssVertexShader(bpy.types.Operator):
    """Give selected meshes the Vertex shader group. This button won't affect meshes without vertex colors, so make sure you've used the Alpha Nodes button before this one."""
    bl_idname = "shdr.vertex"
    bl_label = "Vertex Shader Group"
    
    def execute(self,context):
        button_02(context)
        return{'FINISHED'}

#Button 3
def button_03(context):
    
    #Creating the node inside the material
    sO = bpy.context.selected_objects
    for loopy in sO:
        currentmat = loopy.active_material.node_tree.nodes
        if (currentmat.find('AlphaNode') > -1 or currentmat.find('VertexNode') > -1) and currentmat.find('Image Texture') > -1:
            if currentmat.find('VertexNode') > -1:
                #Find and remove Vertex Node Group
                currentmatdelVRTX = currentmat.get('VertexNode')
                currentmat.remove(currentmatdelVRTX)
            if currentmat.find('AlphaNode') > -1:
                #Find and remove Alpha Node Group
                currentmatdelAlpha = currentmat.get('AlphaNode')
                currentmat.remove(currentmatdelAlpha)
                
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

class clssExport(bpy.types.Operator):
    """Blender can't export materials with shader groups, so use this button before exporting."""
    bl_idname = "shdr.export"
    bl_label = "Remove Groups (for export)"
    
    def execute(self,context):
        button_03(context)
        return{'FINISHED'} 
    
#Color Button       
def button_04(context):
    scn = bpy.context.scene
    scn.view_settings.exposure = 6
    scn.view_settings.gamma = 0.4

            
class clssClr(bpy.types.Operator):
    """Change Exposure and Gamma settings to better match Double Dash's lighting, for more accurate viewport previews in Render mode."""
    bl_idname = "shdr.color"
    bl_label = "Change Exposure & Gamma"
    
    def execute(self,context):
        button_04(context)
        return{'FINISHED'}
        
#--Panel--
from bpy.types import Panel

class SHD_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Auto Shader Nodes"
    bl_category = "ASN"
    
    def draw(self, context):
        
        #Alpha Button
        self.layout.operator("shdr.alpha")
        
        #Vertex Button
        self.layout.operator("shdr.vertex")
        
        #Remove Button
        self.layout.operator("shdr.export")
        
class SHD_PT_Panel2(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Viewport Settings"
    bl_category = "ASN"
    
    def draw(self, context):
        
        #Alpha Button
        self.layout.operator("shdr.color")
        
#--Blender stuff--        
def register():
    bpy.utils.register_class(SHD_PT_Panel)
    bpy.utils.register_class(clssAlphaShader)
    bpy.utils.register_class(clssVertexShader)
    bpy.utils.register_class(clssExport)
    bpy.utils.register_class(SHD_PT_Panel2)
    bpy.utils.register_class(clssClr)

def unregister():
    bpy.utils.register_class(SHD_PT_Panel)
    bpy.utils.register_class(clssAlphaShader)
    bpy.utils.register_class(clssExport)
    bpy.utils.register_class(SHD_PT_Panel2)
    bpy.utils.register_class(clssClr)
    
if __name__ == "__main__":
        register()