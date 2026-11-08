# Mesure, image par image, où passe la main droite pendant les coups (repère du personnage au repos, en % de la hauteur bassin-tête) :
# av < 0 = derrière le plan du dos. Usage : blender -b -P mesure.py -- anim_corps_humain.glb
import bpy, sys
argv = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=argv[0])
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
B = arm.pose.bones; DB = arm.data.bones
U_ = (DB['Head'].head_local - DB['Hips'].head_local).normalized(); G_ = (DB['LeftArm'].head_local - DB['RightArm'].head_local); G_ = (G_ - U_ * G_.dot(U_)).normalized(); A_ = G_.cross(U_)
if (DB['LeftToeBase'].head_local - DB['LeftFoot'].head_local).dot(A_) < 0: A_ = -A_
k = 100 / (DB['Head'].head_local - DB['Hips'].head_local).length
for nom in ('taille', 'revers', 'estoc1'):
    act = next((a for a in bpy.data.actions if a.name.startswith(nom)), None)
    if act is None: print(nom, 'absent'); continue
    arm.animation_data_create(); arm.animation_data.action = act
    f0, f1 = map(int, act.frame_range); print('==', nom)
    for f in range(f0, f1 + 1, 2):
        bpy.context.scene.frame_set(f)
        sp = B['Spine02'].head; dv = B['RightHand'].head - sp; de = B['RightForeArm'].head - sp
        print(f"{f:3d} main av{dv.dot(A_) * k:+.0f} g{dv.dot(G_) * k:+.0f} h{dv.dot(U_) * k:+.0f} | coude av{de.dot(A_) * k:+.0f}")
