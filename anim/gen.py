# Génère les clips d'action pour un modèle riggé : GLB « squelette seul » contenant uniquement les nouvelles animations.
# Usage : blender -b -P gen.py -- modele.glb anim_modele.glb [clip1,clip2,...]   puis   python3 compact.py anim_modele.glb anim_modele.glb
import bpy, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import importlib, animlib as A, clips as C
argv = sys.argv[sys.argv.index('--') + 1:]; src, out = argv[0], argv[1]; only = argv[2].split(',') if len(argv) > 2 and argv[2] else None
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE'); mi = arm.matrix_world.inverted(); zs = []
for o in list(bpy.data.objects):
    if o.type == 'MESH' and o.parent == arm:
        for i in range(0, len(o.data.vertices), 3): zs.append((mi @ (o.matrix_world @ o.data.vertices[i].co)).z)
if zs: zs.sort(); g, top = zs[len(zs) // 400], zs[-1]
else:  # squelette seul (GLB d'animations d'origine) : sol sous les orteils, sommet au-dessus de la tête (seuls les modes 'w'/'h' en dépendent)
    hz = [b.head_local.z for b in arm.data.bones]; g = min(hz); top = max(b.tail_local.z for b in arm.data.bones)
for o in list(bpy.data.objects):
    if o.type != 'ARMATURE': bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
if arm.animation_data: arm.animation_data_clear()
for pb in arm.pose.bones: pb.rotation_mode = 'QUATERNION'
rig = A.Rig(arm, g, top)
arm.animation_data_create()
info = {}
for name, keys in C.CLIPS.items():
    if only and name not in only: continue
    act = A.bake(rig, name, keys, step=2)
    tr = arm.animation_data.nla_tracks.new(); tr.name = name; st = tr.strips.new(name, 0, act); st.name = name
    arm.animation_data.action = None
    info[name] = keys[-1][0]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_animations=True, export_animation_mode='NLA_TRACKS', export_frame_step=2, export_force_sampling=False,
    export_optimize_animation_size=True, export_yup=True, export_apply=False, export_skins=True)
print('GEN', out, json.dumps(info))
