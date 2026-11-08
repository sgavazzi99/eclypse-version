# Clips d'action d'Éclipse (temps en secondes). Unités : bassin/pieds en longueur de jambe, mains 's'/'sw' en longueur de bras,
# 'h'/'w'/'grip'/'o' en hauteur du personnage. Lame = axe de prise de l'arme (vers l'avant de la main).
REL_R = ('s', .12, -.12, -.97); REL_L = ('s', .12, .12, -.97)
ST2 = {'footL': (.12, .03, 0), 'footR': (-.09, -.03, 0)}  # appui : pied gauche devant
def K(t, **p): return (t, p)
def stop(t, **p): p['_stop'] = True; return (t, p)

READY2 = dict(root=(0, 0, -.04), hips=(0, -15, 0), spine=(8, -10, 0), head=(-4, 12, 0), handR=('s', .55, .45, -.55), bladeR=(.55, -.1, .83),
              handL=('mix', ('grip', -.09), REL_L, 0), curlR=85, curlL=85, elbowR=(-.2, -1, -.8), elbowL=(-.2, 1, -.8), **ST2)
CLIPS = {}
CLIPS['lourd'] = [
    stop(0, **READY2),
    stop(.42, root=(-.05, 0, -.06), hips=(-6, -28, 0), spine=(-20, -28, 6), head=(14, 22, 0), handR=('s', .02, .35, .97), bladeR=(-.75, -.12, -.4), elbowR=(0, -1, .5), elbowL=(0, 1, .5)),
    stop(.54, root=(-.055, 0, -.055), handR=('s', -.02, .35, 1.0), spine=(-22, -29, 6)),
    (.72, dict(_stop=True, _ease='in', root=(.10, 0, -.18), hips=(18, 0, 0), spine=(32, 8, 0), head=(-26, -6, 0), handR=('s', .9, .35, -.3), bladeR=(.45, 0, -.9), elbowR=(-.2, -1, -.6), elbowL=(-.2, 1, -.6))),
    stop(.86, root=(.09, 0, -.16), spine=(30, 6, 0), handR=('s', .88, .34, -.33)),
    stop(1.45, **READY2),
]
CLIPS['faucher'] = [
    stop(0, **dict(READY2, bladeR=(.8, -.1, .5))),
    stop(.38, root=(-.03, -.03, -.06), hips=(0, -35, 0), spine=(5, -38, 0), head=(0, 42, 0), handR=('s', .35, -.05, -.45), bladeR=(-.6, -.75, .1), elbowR=(-.5, -1, -.3)),
    K(.56, root=(.04, 0, -.1), hips=(5, 0, 0), spine=(12, 0, 0), head=(-5, 0, 0), handR=('s', .85, .4, -.4), bladeR=(.95, .2, -.1), elbowR=(-.2, -1, -.6)),
    stop(.72, root=(.05, .03, -.08), hips=(5, 35, 0), spine=(8, 40, 0), head=(0, -40, 0), handR=('s', .5, .9, -.3), bladeR=(-.2, 1, 0), elbowR=(-.3, -1, -.4)),
    stop(1.3, **dict(READY2, bladeR=(.8, -.1, .5))),
]
SPEAR = dict(root=(0, 0, -.04), hips=(0, -25, 0), spine=(5, -10, 0), head=(-3, 18, 0), handR=('s', .3, .25, -.75), bladeR=(1, 0, .18), handL=('mix', ('grip', .14), REL_L, 0),
             curlR=85, curlL=85, elbowR=(-.6, -1, -.2), elbowL=(-.2, 1, -.6), **ST2)
CLIPS['estoc'] = [
    stop(0, **SPEAR),
    stop(.28, root=(-.06, 0, -.07), hips=(0, -35, 0), spine=(-3, -20, 0), handR=('s', -.15, .25, -.7)),
    K(.38, footL=(.22, .03, .08)),
    (.46, dict(_stop=True, _ease='out', root=(.16, 0, -.1), hips=(8, -5, 0), spine=(12, 5, 0), head=(-8, 5, 0), handR=('s', .75, .45, -.35), bladeR=(1, 0, .05), footL=(.32, .03, 0))),
    stop(.62, root=(.15, 0, -.1)),
    K(.86, footL=(.22, .03, .07), root=(.06, 0, -.06)),
    stop(1.1, **SPEAR),
]
ONE = dict(root=(0, 0, -.04), hips=(0, -15, 0), spine=(4, -6, 0), head=(-2, 10, 0), handR=('s', .45, .1, -.6), bladeR=(1, 0, .3), handL=('s', .35, -.25, -.6),
           curlR=85, curlL=50, footL=(.1, .03, 0), footR=(-.08, -.03, 0))
CLIPS['estoc1'] = [
    stop(0, **ONE),
    stop(.22, root=(-.04, 0, -.05), hips=(0, -15, 0), spine=(2, -8, 0), handR=('s', .38, -.05, -.38), bladeR=(1, 0, .08), elbowR=(-.2, -1, -.6)),
    K(.3, footL=(.2, .03, .07)),
    (.37, dict(_stop=True, _ease='out', root=(.14, 0, -.1), hips=(6, 5, 0), spine=(10, 10, 0), head=(-8, -8, 0), handR=('s', .98, .28, -.18), bladeR=(1, 0, .02), handL=('s', .1, .2, -.85), footL=(.3, .03, 0))),
    stop(.5, root=(.13, 0, -.1)),
    K(.72, footL=(.2, .03, .06), root=(.05, 0, -.06)),
    stop(.95, **ONE),
]
DAG = dict(root=(0, 0, -.05), hips=(0, -10, 0), spine=(6, 0, 0), handR=('s', .5, .2, -.5), handL=('s', .5, -.2, -.5), bladeR=(1, 0, .3), bladeL=(1, 0, .3),
           curlR=90, curlL=90, footL=(.1, .03, 0), footR=(-.08, -.03, 0))
CLIPS['dagues'] = [
    stop(0, **DAG),
    (.16, dict(_ease='out', handR=('s', .97, .3, -.25), hips=(0, 15, 0), spine=(8, 15, 0), root=(.05, 0, -.07), bladeR=(1, 0, .1))),
    K(.3, handR=('s', .45, .2, -.45), hips=(0, -5, 0), spine=(6, 0, 0)),
    (.42, dict(_ease='out', handL=('s', .97, -.3, -.25), hips=(0, -20, 0), spine=(8, -15, 0), bladeL=(1, 0, .1))),
    K(.56, handL=('s', .45, -.2, -.45), hips=(0, 5, 0), spine=(6, 0, 0), bladeR=(.4, -.9, .2)),
    (.70, dict(_stop=True, _ease='out', handR=('s', .7, .6, -.1), bladeR=(.3, .95, 0), hips=(0, 25, 0), spine=(8, 20, 0), root=(.04, 0, -.07))),
    stop(1.0, **DAG),
]
NOCK = ('o', -.07, 0, 0); ANCRE = ('h', .03, -.08, -.06)
BOW0 = dict(hips=(0, 0, 0), spine=(0, 0, 0), head=(0, 0, 0), handL=('s', .4, .05, -.85), bladeL=(.7, 0, -.7), handR=('mix', REL_R, ('mix', NOCK, ANCRE, 0), 0),
            curlL=95, curlR=40, footL=(.08, .04, 0), footR=(-.06, -.04, 0))
CLIPS['arc'] = [
    stop(0, **BOW0),
    K(.32, hips=(0, -40, 0), spine=(0, -30, 0), head=(0, 62, 0), handL=('sw', .97, -.05, .04), bladeL=(1, 0, 0), handR=('mix', REL_R, ('mix', NOCK, ANCRE, 0), 1), elbowR=(0, -1, .2), curlR=70),
    stop(.9, handR=('mix', REL_R, ('mix', NOCK, ANCRE, 1), 1), elbowR=(-1, -.4, .5)),
    stop(1.0, handR=('mix', REL_R, ('mix', NOCK, ANCRE, 1), 1)),
    (1.06, dict(_stop=True, _ease='out', handR=('mix', REL_R, ('mix', ANCRE, ('h', -.05, -.13, -.04), 1), 1), curlR=10)),
    stop(1.55, **BOW0),
]
GUN0 = dict(hips=(0, -20, 0), spine=(0, -5, 0), head=(0, 15, 0), handR=('s', .35, .3, -.6), bladeR=(.8, 0, -.5), handL=('mix', ('grip', .2), REL_L, 0), curlR=85, curlL=80,
            elbowR=(-.4, -1, -.5), elbowL=(0, 1, -1), footL=(.1, .04, 0), footR=(-.08, -.04, 0))
AIM = dict(handR=('s', .3, .45, -.1), bladeR=(1, 0, 0), head=(5, 25, 0), spine=(0, -12, 0), elbowR=(0, -1, -.1))
CLIPS['tir'] = [
    stop(0, **GUN0), stop(.3, **AIM), stop(.55, **AIM),
    (.6, dict(_stop=True, _ease='out', root=(-.03, 0, 0), spine=(-10, -12, 0), handR=('s', .2, .45, .02), bladeR=(.95, 0, .3))),
    stop(.82, **dict(AIM, root=(0, 0, 0))), stop(1.15, **GUN0),
]
GUARD = dict(root=(0, 0, -.06), hips=(0, -15, 0), spine=(6, -5, 0), handR=('h', .16, -.07, -.13), handL=('h', .19, .07, -.1), bladeR=(0, .2, 1), bladeL=(0, -.2, 1), curlR=105, curlL=105, elbowR=(0, -1, -1), elbowL=(0, 1, -1), footL=(.12, .04, 0), footR=(-.1, -.04, 0))
CLIPS['poings'] = [
    stop(0, **GUARD),
    (.14, dict(_ease='out', handL=('h', .32, .06, -.1), hips=(0, -25, 0))),
    K(.3, handL=('h', .19, .07, -.1), hips=(0, -15, 0)),
    (.45, dict(_ease='out', hips=(0, 30, 0), spine=(6, 15, 0), handR=('h', .33, 0, -.1), root=(.04, 0, -.07))),
    K(.62, handR=('h', .16, -.07, -.13), hips=(0, -10, 0), spine=(6, -5, 0), root=(0, 0, -.06)),
    (.8, dict(_stop=True, _ease='out', hips=(0, -32, 0), spine=(4, -22, 0), handL=('h', .18, -.13, -.1), elbowL=(0, 1, .4))),
    stop(1.2, **GUARD),
]
STAFF0 = dict(handR=('s', .35, .05, -.6), bladeR=(0, 0, 1), handL=('mix', REL_L, ('grip', -.1), 0), curlR=90, curlL=40)
CLIPS['incanter'] = [
    stop(0, **STAFF0),
    K(.5, handR=('s', .3, .2, .85), bladeR=(.2, 0, 1), handL=('mix', REL_L, ('grip', -.1), 1), spine=(-12, 0, 0), head=(-14, 0, 0), curlL=85, elbowR=(0, -1, .3), elbowL=(0, 1, .3)),
    stop(.66, handR=('s', .3, .2, .9), spine=(-14, 0, 0)),
    (.85, dict(_stop=True, _ease='in', root=(.03, 0, -.14), spine=(25, 0, 0), head=(-15, 0, 0), handR=('s', .6, .25, -.45), bladeR=(.25, 0, 1), footL=(.1, .03, 0), footR=(-.08, -.03, 0), elbowR=(-.3, -1, -.5), elbowL=(-.3, 1, -.5))),
    stop(1.0, root=(.03, 0, -.13)),
    stop(1.6, **dict(STAFF0, root=(0, 0, 0), spine=(0, 0, 0), head=(0, 0, 0), footL=(0, 0, 0), footR=(0, 0, 0))),
]
SH0 = dict(root=(0, 0, -.08), spine=(8, -8, 0), hips=(0, -12, 0), handL=('s', .55, -.15, -.15), bladeL=(0, 0, 1), handR=('s', .5, .25, -.4), bladeR=(.6, -.3, .75),
           curlR=85, curlL=80, footL=(.12, .04, 0), footR=(-.1, -.04, 0), head=(-6, 10, 0))
CLIPS['garde'] = [stop(0), (.3, dict(SH0, _stop=True, _ease='out')), stop(.6, **SH0)]
CLIPS['saut'] = [
    stop(0),
    stop(.12, root=(0, 0, -.13), spine=(16, 0, 0), head=(-10, 0, 0), handR=('s', -.4, -.05, -.8), handL=('s', -.4, .05, -.8)),
    (.26, dict(_ease='out', root=(0, 0, .03), spine=(-4, 0, 0), handR=('s', .55, -.05, .1), handL=('s', .55, .05, .1), toeL=-30, toeR=-30, footrotL=(-25, 0, 0), footrotR=(-25, 0, 0))),
    stop(.55, root=(0, 0, .05), spine=(8, 0, 0), footL=(.12, 0, .3), footR=(-.06, 0, .18), toeL=0, toeR=0, footrotL=(10, 0, 0), footrotR=(15, 0, 0), handR=('s', .4, -.1, -.2), handL=('s', .4, .1, -.2)),
]
CLIPS['roulade'] = [
    stop(0, feetrel=True),
    K(.1, feetrel=True, root=(.05, 0, -.3), hips=(45, 0, 0), spine=(40, 0, 0), head=(30, 0, 0), handR=('s', .9, .2, -.4), handL=('s', .9, -.2, -.4), footL=(0, 0, .25), footR=(0, 0, .25)),
    K(.32, feetrel=True, root=(0, 0, -.62), hips=(180, 0, 0), spine=(60, 0, 0), head=(45, 0, 0), footL=(-.1, 0, .6), footR=(-.1, 0, .6), handR=('s', .3, .4, -.5), handL=('s', .3, -.4, -.5)),
    K(.52, feetrel=True, root=(0, 0, -.35), hips=(300, 0, 0), spine=(35, 0, 0), head=(20, 0, 0), footL=(0, 0, .35), footR=(0, 0, .3)),
    stop(.72, feetrel=True, root=(0, 0, 0), hips=(360, 0, 0), spine=(0, 0, 0), head=(0, 0, 0), footL=(0, 0, 0), footR=(0, 0, 0), handR=REL_R, handL=REL_L),
]
CLIPS['recolte'] = [
    stop(0),
    stop(.55, root=(0, 0, -.38), hips=(25, 0, 0), spine=(32, 0, 0), head=(-22, 0, 0), footL=(.12, .03, 0), footR=(-.12, -.03, 0), handR=('w', .3, -.05, .04), curlR=30, kneeL=(1, .3, 0), kneeR=(1, -.3, 0)),
    stop(.9, curlR=100, handR=('w', .3, -.05, .05)),
    K(1.3, root=(0, 0, -.1), hips=(5, 0, 0), spine=(8, 0, 0), head=(0, 0, 0), handR=('s', .45, .15, -.45)),
    stop(1.8, root=(0, 0, 0), hips=(0, 0, 0), spine=(0, 0, 0), handR=REL_R, curlR=25, footL=(0, 0, 0), footR=(0, 0, 0)),
]

# ---- 0.16 : coups à une main, sorts, blocage, dégainer ----
# 0.4.1 : combo de l'épée refait (demande de Simon) — 1) diagonale du haut à droite vers le bas à gauche, 2) horizontale de gauche
# à droite, 3) estoc droit devant. Le tronc tourne moins (30° au lieu de 65°) et le coude reste sur le côté ou devant : la main ne
# passe plus jamais derrière le dos. Mesuré dans Blender (tools/blender/anim/mesure.py) : la main ne passe plus jamais derrière
# le plan du dos (ancien combo : jusqu'à 75 % de la longueur du tronc derrière). Valeurs PROVISOIRES (pas encore testées en jeu).
CLIPS['taille'] = [
    stop(0, **ONE),
    stop(.24, root=(-.03, 0, -.05), hips=(0, -15, 0), spine=(-4, -15, 2), head=(0, 14, 0), handR=('s', .62, -.2, .55), bladeR=(.1, -.35, .93), elbowR=(.5, -1, .3), handL=('s', .35, -.05, -.5)),
    K(.33, root=(.06, 0, -.08), hips=(3, 2, 0), spine=(6, 2, -1), head=(-4, -2, 0), handR=('s', .8, .1, .1), bladeR=(.75, .3, .55), elbowR=(0, -1, -.3)),
    (.42, dict(_stop=True, _ease='in', root=(.12, 0, -.1), hips=(6, 18, 0), spine=(14, 16, -4), head=(-8, -14, 0), handR=('s', .72, .5, -.48), bladeR=(.5, .6, -.62), elbowR=(-.1, -1, -.6), handL=('s', .2, .15, -.7), footL=(.24, .03, 0))),
    stop(.54, root=(.11, 0, -.1)),
    K(.76, footL=(.14, .03, .05), root=(.04, 0, -.06)),
    stop(1.0, **ONE),
]
CLIPS['revers'] = [
    stop(0, **ONE),
    stop(.22, root=(-.02, 0, -.05), hips=(0, 15, 0), spine=(3, 15, 0), head=(0, -14, 0), handR=('s', .58, .5, -.08), bladeR=(-.1, .97, .15), elbowR=(.7, -.3, -.6), handL=('s', .25, .3, -.6)),
    K(.31, root=(.04, -.01, -.07), hips=(2, 0, 0), spine=(5, 0, 0), head=(-2, 0, 0), handR=('s', .88, .05, -.1), bladeR=(.97, .15, .05), elbowR=(.2, -1, -.6)),
    (.40, dict(_stop=True, _ease='in', root=(.08, -.03, -.08), hips=(4, -18, 0), spine=(6, -18, 0), head=(-4, 16, 0), handR=('s', .78, -.48, -.12), bladeR=(.35, -.93, .05), elbowR=(0, -1, -.6), footR=(-.05, -.08, 0))),
    stop(.52, root=(.08, -.03, -.08)),
    stop(.9, **ONE),
]
CAST0 = dict(root=(0, 0, -.03), hips=(0, -10, 0), spine=(4, -5, 0), handR=('s', .3, .05, -.65), bladeR=(.6, 0, .8), handL=('s', .3, -.15, -.6), curlL=20, curlR=85, footL=(.08, .04, 0), footR=(-.06, -.04, 0))
CLIPS['lancer'] = [
    stop(0, **CAST0),
    stop(.28, root=(-.04, 0, -.05), hips=(0, -30, 0), spine=(-6, -25, 0), head=(0, 25, 0), handL=('s', .05, .1, .15), curlL=60, elbowL=(-.5, 1, -.2)),
    (.42, dict(_stop=True, _ease='out', root=(.1, 0, -.08), hips=(4, 15, 0), spine=(10, 12, 0), head=(-5, -10, 0), handL=('s', .98, -.15, .15), curlL=0, elbowL=(0, 1, -.4), footL=(.2, .04, 0))),
    stop(.6, root=(.09, 0, -.08)),
    stop(1.0, **CAST0),
]
CLIPS['soin'] = [
    stop(0, **CAST0),
    K(.35, root=(0, 0, -.06), spine=(-8, 0, 0), head=(-12, 0, 0), handL=('s', .55, -.05, .25), handR=('s', .5, .1, .2), curlL=5, elbowL=(-.5, 1, -.3)),
    stop(.7, root=(0, 0, .02), spine=(-14, 0, 0), head=(-22, 0, 0), handL=('s', .35, -.45, .8), curlL=0, handR=('s', .4, .3, .5)),
    stop(.9, spine=(-14, 0, 0)),
    stop(1.4, **CAST0),
]
CLIPS['bloquer'] = [
    stop(0, **ONE),
    (.18, dict(_stop=True, _ease='out', root=(-.02, 0, -.08), hips=(0, -20, 0), spine=(4, -8, 0), handR=('s', .5, .35, .3), bladeR=(.1, .98, .15), elbowR=(-.2, -1, -.3), handL=('s', .55, -.05, .05), bladeL=(0, 0, 1), curlL=95, footL=(.14, .05, 0), footR=(-.1, -.04, 0))),
    stop(1.0, root=(-.02, 0, -.08)),
]
CLIPS['degainer_h'] = [
    stop(0),
    (.22, dict(_stop=True, _ease='out', spine=(6, 12, 0), hips=(0, 8, 0), head=(-6, -10, 0), handR=('s', .2, .55, -.95), curlR=95, elbowR=(-.6, -1, -.2))),
    stop(.3, handR=('s', .22, .55, -.95)),
    (.55, dict(_stop=True, _ease='out', **ONE)),
    stop(.8, **ONE),
]
CLIPS['degainer_d'] = [
    stop(0, bladeR=(.2, 0, -1), handL=('mix', ('grip', -.09), REL_L, 0)),
    (.25, dict(_stop=True, _ease='out', spine=(-6, -8, 0), head=(4, 10, 0), handR=('s', -.25, .05, .55), curlR=95, elbowR=(.2, -1, .8))),
    stop(.33, handR=('s', -.25, .06, .56)),
    (.6, dict(_stop=True, _ease='out', **READY2)),
    stop(.85, **READY2),
]

# ---- 0.16b : postures de combat tenues (une main sans bouclier, deux mains) — la main libre reste détendue le long du corps ----
ONE_G = dict(ONE, handL=('s', .18, .1, -.95), curlL=30, elbowL=(-.3, 1, -.6))
CLIPS['garde1'] = [stop(0), (.3, dict(ONE_G, _stop=True, _ease='out')), stop(.6, **ONE_G)]
CLIPS['garde2'] = [stop(0), (.3, dict(READY2, _stop=True, _ease='out')), stop(.6, **READY2)]
