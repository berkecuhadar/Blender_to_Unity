bl_info = {
    "name": "To Unity 6 FBX",
    "author": "Berke CUHADAR",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > To Unity FBX",
    "description": "Unity 6 optimized FBX exporter with presets",
    "category": "Import-Export",
}

import bpy
from bpy.props import BoolProperty, FloatProperty, StringProperty
from bpy.types import Operator, Panel


# ======================================================
#  MAIN EXPORT FUNCTION
# ======================================================
def export_unity_fbx(filepath, include_rig, include_anim, scale, all_actions):
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
        mesh_smooth_type='FACE',

        # Bones
        add_leaf_bones=False,
        armature_nodetype='NULL',
        use_armature_deform_only=True,

        # Animations
        bake_anim=include_anim,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=all_actions,
        bake_anim_force_startend_keying=True,
        bake_anim_simplify_factor=0.0,
    )


# ======================================================
#  EXPORT OPERATOR (presets and custom share this)
# ======================================================
class TOUNITY_OT_Export(Operator):
    bl_idname = "object.to_unity_export"
    bl_label = "Export Unity FBX"
    bl_description = "Export the selection as a Unity-ready FBX"

    filepath: StringProperty(subtype="FILE_PATH", options={'HIDDEN'})
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})
    include_rig: BoolProperty(name="Include Rig", default=True)
    include_anim: BoolProperty(name="Include Animations", default=True)
    all_actions: BoolProperty(
        name="All Actions",
        description="Export every action in the file, not only the active one / NLA strips",
        default=False,
    )
    scale: FloatProperty(name="Global Scale", default=1.0, min=0.0001)

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        if self.include_rig and not any(o.type == 'ARMATURE' for o in selected):
            self.report({'WARNING'}, "No armature selected, exporting meshes only")

        path = bpy.path.ensure_ext(self.filepath, ".fbx")
        try:
            export_unity_fbx(path, self.include_rig, self.include_anim,
                             self.scale, self.all_actions)
        except RuntimeError as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

        # Remember target + settings so "Update Last Export" can overwrite it
        scene = context.scene
        scene.to_unity_last_path = path
        scene.to_unity_last_rig = self.include_rig
        scene.to_unity_last_anim = self.include_anim

        self.report({'INFO'}, f"Exported to: {path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            last = context.scene.to_unity_last_path
            if last:
                self.filepath = last
            else:
                name = bpy.path.display_name_from_filepath(bpy.data.filepath) or "untitled"
                self.filepath = f"{name}.fbx"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# ======================================================
#  UPDATE OPERATOR (overwrite last export, keeps Unity GUID)
# ======================================================
class TOUNITY_OT_Update(Operator):
    bl_idname = "object.to_unity_update"
    bl_label = "Update Last Export"
    bl_description = ("Re-export to the same file with the same settings. "
                      "Overwriting keeps the Unity .meta file, so the GUID and references stay intact")

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) and bool(context.scene.to_unity_last_path)

    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.to_unity_last_path)
        try:
            export_unity_fbx(path, scene.to_unity_last_rig, scene.to_unity_last_anim,
                             scene.to_unity_scale, scene.to_unity_all_actions)
        except RuntimeError as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Updated: {path}")
        return {'FINISHED'}


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
        scene = context.scene

        layout.prop(scene, "to_unity_scale")
        layout.prop(scene, "to_unity_all_actions")

        layout.label(text="Presets")
        col = layout.column(align=True)
        presets = (
            ("Static Mesh (No Rig/Anim)", False, False),
            ("Rigged (No Anim)", True, False),
            ("Rigged + Animations", True, True),
        )
        for label, rig, anim in presets:
            op = col.operator(TOUNITY_OT_Export.bl_idname, text=label)
            op.include_rig = rig
            op.include_anim = anim
            op.scale = scene.to_unity_scale
            op.all_actions = scene.to_unity_all_actions

        layout.separator()
        layout.label(text="Custom Export")
        layout.operator(TOUNITY_OT_Export.bl_idname, text="Manual Settings")

        layout.separator()
        layout.label(text="Update")
        layout.prop(scene, "to_unity_last_path", text="")
        layout.operator(TOUNITY_OT_Update.bl_idname, icon='FILE_REFRESH')


# ======================================================
#  REGISTER
# ======================================================
classes = (
    TOUNITY_OT_Export,
    TOUNITY_OT_Update,
    TOUNITY_PT_Panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.to_unity_scale = FloatProperty(
        name="Global Scale", default=1.0, min=0.0001)
    bpy.types.Scene.to_unity_all_actions = BoolProperty(
        name="Export All Actions", default=False)
    bpy.types.Scene.to_unity_last_path = StringProperty(
        name="Last Export", subtype="FILE_PATH")
    bpy.types.Scene.to_unity_last_rig = BoolProperty(default=True)
    bpy.types.Scene.to_unity_last_anim = BoolProperty(default=True)


def unregister():
    del bpy.types.Scene.to_unity_last_anim
    del bpy.types.Scene.to_unity_last_rig
    del bpy.types.Scene.to_unity_last_path
    del bpy.types.Scene.to_unity_all_actions
    del bpy.types.Scene.to_unity_scale
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
