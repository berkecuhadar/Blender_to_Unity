bl_info = {
    "name": "To Unity FBX",
    "author": "Berke CUHADAR",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > To Unity FBX",
    "description": "Export selected objects as Unity-compatible FBX",
    "category": "Import-Export",
}

import bpy
import os
from math import radians
from bpy.props import StringProperty
from bpy.types import Operator, Panel

class ToUnityFBXExportOperator(Operator):
    bl_idname = "object.to_unity_fbx_export"
    bl_label = "To Unity FBX Export"
    bl_description = "Export selected objects as FBX with Unity-compatible settings"
    
    filepath: StringProperty(
        name="Export Path",
        description="Path to export FBX file",
        default="",
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        if not bpy.context.selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Ensure file has .fbx extension
        export_path = self.filepath if self.filepath.lower().endswith(".fbx") else f"{self.filepath}.fbx"
        if not self.filepath:
            export_path = os.path.join(os.path.expanduser("~"), "exported_object.fbx")
        
        # Export FBX with Unity-compatible settings
        bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection=True,
            global_scale=1.0,
            axis_forward='-Z',
            axis_up='Y',
            apply_unit_scale=True,
            bake_space_transform=True,  # Bake transformations into the FBX file
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'MESH', 'ARMATURE'},
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_subsurf=False,
            use_mesh_edges=False,
            use_tspace=False
        )
        
        self.report({'INFO'}, f"Exported to: {export_path}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ToUnityFBXExportPanel(Panel):
    bl_label = "To Unity FBX Export"
    bl_idname = "VIEW3D_PT_to_unity_fbx_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'To Unity FBX'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(ToUnityFBXExportOperator.bl_idname)

def register():
    bpy.utils.register_class(ToUnityFBXExportOperator)
    bpy.utils.register_class(ToUnityFBXExportPanel)

def unregister():
    bpy.utils.unregister_class(ToUnityFBXExportOperator)
    bpy.utils.unregister_class(ToUnityFBXExportPanel)

if __name__ == "__main__":
    register()
