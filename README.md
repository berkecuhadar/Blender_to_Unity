# Blender_to_Unity
 A Blender addon to easily export selected objects as FBX files with Unity-compatible settings. Features include baked transforms, correct axis orientation, and support for mesh and armature objects. Perfect for workflows involving Unity and tools like Mixamo. Compatible with Blender 4.0.0 and above. 🚀

## Features
- Export selected objects as FBX.
- Automatically applies transformations for Unity compatibility.
- Supports mesh and armature objects.
- Configurable export path via a file browser.

## Installation
1. Download the addon as a `.zip` file.
2. Open Blender and navigate to `Edit > Preferences > Add-ons`.
3. Click **Install...**, select the downloaded `.zip` file, and click **Install from Disk**.
4. Enable the addon by checking the box next to `To Unity FBX`.

## Usage
1. In the 3D View, select the objects you want to export.
2. Open the sidebar (`N` key) and navigate to the **To Unity FBX** tab.
3. Click the **To Unity FBX Export** button.
4. Choose the export path using the file browser.
5. Click **Export** to save the FBX file.

## Workflow Example
1. A rigless mesh was exported to Unity using this addon and confirmed to be correctly imported.
2. The exported mesh was uploaded to Mixamo, where animations were added.
3. The animated mesh was imported back into Blender for further adjustments to the animation.
4. The updated animation was exported again using this addon and imported into Unity, where it worked as expected.

## Settings
The addon exports objects with the following settings:
- **Scale**: 1.0
- **Forward Axis**: `-Z`
- **Up Axis**: `Y`
- **Unit Scale Applied**
- **Transforms Baked**
- Supports **Mesh** and **Armature** objects.

## Requirements
- Blender 4.0.0 or higher.

## Author
- **Name**: Berke Cuhadar
- **Version**: 1.0

## License
This addon is distributed under the [MIT License](https://opensource.org/licenses/MIT).
