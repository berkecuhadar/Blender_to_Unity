# Changelog

## v1.2 (LATEST)

### Added
- Global Scale and "Export All Actions" options in the panel, applied to all presets.
- Warning when a rig preset is used without an armature selected.

- **Update Last Export** button: overwrites the previous FBX with the same settings in one click.
  Because the file path stays the same, Unity keeps the `.meta` file and the GUID, so prefabs and scene references don't break.
  The last path and settings are saved inside the `.blend` file.

### Improved
- Merged the four export operators into one shared operator (less code, same behavior).
- Export buttons are disabled when nothing is selected (Custom Export included).
- Export errors are reported instead of raising a traceback.
- Smoothing now uses `FACE` instead of `OFF` so normals export correctly.
- Only the active action / NLA strips are exported by default (no more file bloat).
- Add-on moved into a `to_unity_fbx/` folder so zipping it installs correctly.
- Removed the duplicate changelog from the source file.

## v1.1

### Added
- Export presets:
  - **Static Mesh** (no rig, no animation)
  - **Rigged (No Anim)**
  - **Rigged + Animations**
- Custom Export operator with adjustable:
  - Rig inclusion
  - Animation exporting
  - Global scale

### Improved
- Unified all FBX export logic into a single shared function for cleaner structure.
- Enhanced Unity 6 compatibility:
  - Correct axis orientation (`-Z Forward`, `Y Up`)
  - Stable global scaling
  - Predictable transform baking

### Fixed / Optimized
- Disabled leaf bones (removes unnecessary "end" bones).
- Export now includes only deform bones for cleaner, lighter rigs.
- More stable animation baking:
  - Forced start/end keyframes
  - No simplification artifacts
