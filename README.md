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

* **Vertex Transparency Shader Group:** Creates a node group in the active material of all selected meshess, which allows you to see texture transparency and vertex colors *with their transparency data*. This button does nothing if the mesh doesn't contain vertex colors *and* if the material doesn't have a texture.

* **Remove Groups (for export):** Blender can't export materials with shader node groups, so use this button to remove groups from the materials of all selected meshes. ***NO LONGER NEEDED IF USING THE NEW EXPORT BUTTONS***

### Viewport Settings

* **Change Exposure & Gamma:** Change Exposure and Gamma settings to better match Double Dash's lighting, for more accurate viewport previews in Render mode.
### Export

* **Course Name:** Gives your exports a name. You only need to add the course's unique identifier, so *don't* add `_course` to the name. Just call it `luigi`, or `rainbow`, for example.

* **Export Selection as DAE:** Exports all selected objects to a file named `[coursename]_course.dae` inside a folder called `course` (will be created if it doesn't exist) inside the directory where the current Blender file is saved.

* **Export Selecttion as OBJ:** Exports all selected objects as a file called `[coursename]_course.obj` to a folder called `course_collision` (will be created if it doesn't exist) inside the directory where the current Blender file is saved.

These buttons export with default settings, except for `Selection Only` and `Triangulate`, which are on for convenience.

Your directory would look like this after exporting with the buttons:
```
c:/my/files
├───course
│   ├───[coursename]_course.dae
│   └───textures.png
├───course_collision
│   └───[coursename]_course.obj
└───myBlenderFile.blend
```

### Collision Tools

* **Remove Vertical Geometry:** Automatically removes all vertical geometry in the selected objects. Adjusting the `Strength` setting will alter how generous it is towards deleting slanted geometry. Using the default `0.63` is recommended.

* **Roadtype Info:** Clicking the button will display the type of collision for the currently active material. For example, selecting the material `Roadtype_0x0200` would display `Kart and item wall`.

### Misc. info

1. You can quickly swap node groups by just clicking the button of the node you wanna replace it with.

1. If you wanna apply these settings to all selected meshes, I recommend clicking the `Alpha Shader Group button` first and then the `Vertex Shader Group` button. This way every object on your scene (assuming they have image textures) will have a Node Group applied.

1. Most buttons (except for `Change Exposure & Gamma`) will give you an error if you click them non-mesh objects or meshes without materials are selected.