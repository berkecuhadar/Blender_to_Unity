# Blender to Unity 6 – FBX Export Add-on

A Blender add-on designed for clean and optimized FBX export workflows targeting **Unity 6**.  
Includes one-click presets, correct axis orientation, baked transforms, deform-only rigs, and optional animation export.  
Perfect for pipelines involving Unity, Mixamo, game-ready rigs, and character animation. 🚀

---

## ✨ Features
- ✔ One-click export presets:
  - **Static Mesh** (no rig, no animation)
  - **Rigged (No Animation)**
  - **Rigged + Animations**
- ✔ Custom export option with adjustable settings
- ✔ Correct Unity-compatible orientation (**-Z Forward**, **Y Up**)  
- ✔ Clean rigs (no leaf/end bones, deform-only)
- ✔ Supports Mesh + Armature objects
- ✔ Baked transforms and stable scale handling
- ✔ Compatible with **Blender 4.0+**

---

## 📥 Installation
1. Download the add-on as a `.zip`.
2. Open Blender → **Edit > Preferences > Add-ons**.
3. Click **Install…**, select the `.zip`, and confirm.
4. Enable the add-on: **To Unity FBX**.

---

## ▶ Usage
1. Select the objects you want to export.
2. Press **N** to open the sidebar → **To Unity FBX** tab.
3. Choose a preset:
   - Static Mesh  
   - Rigged (No Anim)  
   - Rigged + Animations  
4. Or use **Custom Export** for manual configuration.
5. Choose the export path.
6. Export → Unity-ready FBX is generated.

---

## 🛠 Example Workflow
1. Export a mesh or rig from Blender using this add-on.  
2. Import into Unity → confirm correct orientation & scale.  
3. (Optional) Upload to Mixamo to add animations.  
4. Download and re-import into Blender for fine-tuning.  
5. Re-export using **Rigged + Animations** preset.  
6. Import into Unity → animations work immediately.  

---

## ⚙ Default Export Settings
- **Scale:** 1.0  
- **Forward Axis:** `-Z`  
- **Up Axis:** `Y`  
- **Transform Baking:** Enabled  
- **Unit Scale:** Applied  
- **Leaf Bones:** Removed  
- **Meshes + Armatures:** Supported  
- **Animations:** Optional (based on preset)

---

## 📦 Requirements
- Blender **4.0.0+**

---

## 👤 Author
**Berke Cuhadar**  
Version **1.1**

---

## 📄 License
Distributed under the **MIT License**.  
See: https://opensource.org/licenses/MIT
