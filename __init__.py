bl_info = {
    "name": "To Unity 6 FBX",
    "author": "Berke CUHADAR",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > To Unity FBX",
    "description": "Unity 6 optimized FBX exporter with presets",
    "category": "Import-Export",
}

import bpy
import os
from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import Operator, Panel


# ======================================================
#  MAIN EXPORT FUNCTION (used by presets)
# ======================================================
def export_unity_fbx(filepath, include_rig, include_anim, scale):
    # Object types
    obj_types = {"MESH"}
    if include_rig:
        obj_types.add("ARMATURE")

    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,

        # Scale & orientation for Unity
        global_scale=scale,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=True,

        # Object types
        object_types=obj_types,
        use_mesh_modifiers=True,
        mesh_smooth_type='OFF',

        # Bones
        add_leaf_bones=False,
        armature_nodetype='NULL',
        use_armature_deform_only=True,

        # Animations
        bake_anim=include_anim,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=True,
        bake_anim_force_startend_keying=True,
        bake_anim_simplify_factor=0.0,
    )


# ======================================================
#  BASE OPERATOR
# ======================================================
class TOUNITY_OT_BaseExport(Operator):
    bl_idname = "object.to_unity_base_export"
    bl_label = "Unity FBX Export Base"

    filepath: StringProperty(subtype="FILE_PATH")
    include_rig: BoolProperty()
    include_anim: BoolProperty()
    scale: FloatProperty()

    def execute(self, context):
        if not bpy.context.selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        export_path = (
            self.filepath if self.filepath.lower().endswith(".fbx")
            else f"{self.filepath}.fbx"
        )

        export_unity_fbx(
            filepath=export_path,
            include_rig=self.include_rig,
            include_anim=self.include_anim,
            scale=self.scale,
        )

        self.report({'INFO'}, f"Exported to: {export_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# ======================================================
#  PRESET OPERATORS
# ======================================================
class TOUNITY_OT_StaticMesh(Operator):
    bl_idname = "object.to_unity_static_mesh"
    bl_label = "Static Mesh (No Rig/Anim)"

    def invoke(self, context, event):
        op = bpy.ops.object.to_unity_base_export
        return op("INVOKE_DEFAULT",
                  include_rig=False,
                  include_anim=False,
                  scale=1.0)


class TOUNITY_OT_RigNoAnim(Operator):
    bl_idname = "object.to_unity_rig_no_anim"
    bl_label = "Rigged (No Anim)"

    def invoke(self, context, event):
        op = bpy.ops.object.to_unity_base_export
        return op("INVOKE_DEFAULT",
                  include_rig=True,
                  include_anim=False,
                  scale=1.0)


class TOUNITY_OT_RigWithAnim(Operator):
    bl_idname = "object.to_unity_rig_anim"
    bl_label = "Rigged + Animations"

    def invoke(self, context, event):
        op = bpy.ops.object.to_unity_base_export
        return op("INVOKE_DEFAULT",
                  include_rig=True,
                  include_anim=True,
                  scale=1.0)


# ======================================================
#  MANUAL EXPORT OPERATOR (with options)
# ======================================================
class TOUNITY_OT_CustomExport(Operator):
    bl_idname = "object.to_unity_custom_export"
    bl_label = "Custom Unity FBX Export"

    filepath: StringProperty(subtype="FILE_PATH")
    include_rig: BoolProperty(name="Include Rig", default=True)
    include_anim: BoolProperty(name="Include Animations", default=True)
    scale: FloatProperty(name="Global Scale", default=1.0)

    def execute(self, context):
        export_path = (
            self.filepath if self.filepath.lower().endswith(".fbx")
            else f"{self.filepath}.fbx"
        )

        export_unity_fbx(export_path, self.include_rig,
                         self.include_anim, self.scale)

        self.report({'INFO'}, f"Exported to: {export_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# ======================================================
#  PANEL
# ======================================================
class TOUNITY_PT_Panel(Panel):
    bl_label = "To Unity 6 FBX"
    bl_idname = "VIEW3D_PT_to_unity_fbx_export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "To Unity FBX"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Presets")

        # Preset buttons
        col = layout.column(align=True)
        col.operator("object.to_unity_static_mesh", text="Static Mesh (No Rig/Anim)")
        col.operator("object.to_unity_rig_no_anim", text="Rigged (No Anim)")
        col.operator("object.to_unity_rig_anim", text="Rigged + Animations")

        layout.separator()

        layout.label(text="Custom Export")
        layout.operator("object.to_unity_custom_export", text="Manual Settings")


# ======================================================
#  REGISTER
# ======================================================
classes = (
    TOUNITY_OT_BaseExport,
    TOUNITY_OT_StaticMesh,
    TOUNITY_OT_RigNoAnim,
    TOUNITY_OT_RigWithAnim,
    TOUNITY_OT_CustomExport,
    TOUNITY_PT_Panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()


# ======================================================
# CHANGELOG
# ======================================================
# v1.1 (LATEST)
# 
# ADDED
# - Added three export presets:
#     * Static Mesh (no rig, no animation)
#     * Rigged (no animation)
#     * Rigged + Animations
# - Added Custom Export operator with adjustable rig, animation, and scale settings.
#
# IMPROVED
# - Centralized the FBX export logic into a single shared function for cleaner structure.
# - Improved Unity 6 compatibility:
#     * Correct axis orientation (-Z Forward, Y Up)
#     * Stable global scaling
#     * More predictable transform baking
#
# FIXED / OPTIMIZED
# - Disabled leaf bones to remove unnecessary 'end' bones.
# - Only deform bones are exported (cleaner and lighter rigs).
# - Improved animation baking: stable keyframes and no simplification issues.

