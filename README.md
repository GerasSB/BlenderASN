# Auto Shader Nodes for Blender

Specifically created for Double Dash modding, this plugin creates shader node groups that allow you to preview alpha textures and vertex colors, as well as changing the scene's Gamma and Exposure to better match in-game lighting.

## Demo
https://user-images.githubusercontent.com/19808950/228373866-43a6f2f2-b21f-4834-968e-75b0c64e1975.mp4

## How to install
Go [here](https://raw.githubusercontent.com/GerasSB/BlenderASN/main/auto_shader_pnl.py), right click the page and select *Save As...* to download the script from the repo. Go to *Blender > Edit > Preferences* and in the Add-ons pane click on *Install...*. Select the file you just downloaded and enable it by clicking the checkbox.

## How to use

In the 3D viewport, you'll find a new panel within the N menu called ASN. That panel contains everything you can do with this plugin.

### Auto Shader Nodes
* **Alpha Shader Group:** Creates a node group in the active material of all selected meshes, which allows you to see texture transparency. This button does nothing if the material doesn't have a texture.

* **Vertex Shader Group:** Creates a node group in the active material of all selected meshes, which allows you to see texture transparency and vertex colors. This button does nothing if the mesh doesn't contain vertex colors *and* if the material doesn't have a texture.

* **Remove Groups (for export):** Blender can't export materials with shader node groups, so use this button to remove groups from the materials of all selected meshes.

You can quickly swap node groups by just clicking the button of the node you wanna replace it with.

**These buttons will give you an error if you try to apply them on non-mesh objects.**

### Viewport Settings

* **Change Exposure & Gamma:** Change Exposure and Gamma settings to better match Double Dash's lighting, for more accurate viewport previews in Render mode.
