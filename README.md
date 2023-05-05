# Auto Shader Nodes for Blender

Specifically created for Double Dash track creation, this plugin adds several new features to help make the process more efficient.

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

* **Remove Groups (for export):** Blender can't export materials with shader node groups, so use this button to remove groups from the materials of all selected meshes. ***NO LONGER NEEDED IF USING THE NEW EXPORT BUTTONS.***

### Viewport Settings

* **Change Exposure & Gamma:** Change Exposure and Gamma settings to better match Double Dash's lighting, for more accurate viewport previews in Render mode.
### Export

* **Course Name:** Gives your exports a name. You only need to add the course's unique identifier, so *don't* add `_course` to the name. Just call it `luigi`, or `rainbow`, for example.

* **Export Selection as DAE:** Exports all selected objects to a file named `[coursename]_course.dae` inside a folder called `course` (will be created if it doesn't exist) inside the directory where the current Blender file is saved. Textures are also put in the same folder.

* **Export Selecttion as OBJ:** Exports all selected objects as a file called `[coursename]_course.obj` to a folder called `course_collision` (will be created if it doesn't exist) inside the directory where the current Blender file is saved.

These buttons export with default settings, except for `Selection Only` and `Triangulate`, which are on for convenience.

Any selected non-mesh object is automatically excluded from exports (this includes any mesh with an armature). Meshes with the word `EXCLUDE` somewhere in their name are also excluded from exports, which can be useful for an easier non-destructive workflow when using modifiers.

All meshes must have a material assigned or the export will be aborted, providing an error message with the name of the mesh that's missing materials.

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

* **Select Vertical Geometry:** Automatically selects all vertical geometry in the selected objects. Adjusting the `Strength` setting will alter how generous it is towards selecting slanted geometry (the lower, the more vertical the geometry has to be for it to be selected).
    * The default (`0.5`) is the steepest a *wall* has been observed to be in vanilla courses.
    * The lowest (`0.37`) is the steepest a *road* has been observed to be in vanilla courses.

* **Roadtype Info:** Clicking the button will display the following information for the currently active material:
    * Collision type. For example, selecting the material `Roadtype_0x0200` would display `Kart and item wall`
    * Respawn ID
    * Falling animation enabled/disabled
    * GeoSplash index

### Misc. tips

1. You can quickly swap node groups by selecting an object and clicking the button of the node you wanna replace it with.

1. If you wanna preview your whole model to what it's gonna look like in game, I recommend selecting your whole model, clicking the `Alpha Shader Group button` first and then the `Vertex Shader Group` button. This way every object on your scene (assuming they have image textures) will have a Node Group applied.

1. Most buttons (except for `Change Exposure & Gamma`) will give you an error if meshes without materials are selected.