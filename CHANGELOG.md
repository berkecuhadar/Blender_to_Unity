# Changelog

## v1.1 (LATEST)

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
