# Éclipse — bibliothèque d'animation procédurale pour le squelette Meshy (24 os + doigts).
# Les poses sont décrites en intentions (position des mains, des pieds, orientation de l'arme, inclinaison du buste)
# et résolues par IK analytique sur le squelette réel de chaque modèle : pieds plantés, deux mains sur le manche.
import bpy, math
from mathutils import Vector, Quaternion, Matrix
FPS = 24
F = Vector((0, -1, 0)); L = Vector((1, 0, 0)); U = Vector((0, 0, 1))
def ch(v): return Vector((v[1], -v[0], v[2]))  # (avant, gauche, haut) -> espace armature
def rad(d): return d * math.pi / 180
def rotq(e):
    p, y, r = (list(e) + [0, 0, 0])[:3]
    return Quaternion(U, rad(y)) @ Quaternion(L, rad(p)) @ Quaternion(Vector((0, -1, 0)), rad(r))
def frame(a, b):
    a = a.normalized(); b = (b - a * b.dot(a)); b = b.normalized() if b.length > 1e-6 else a.orthogonal().normalized()
    return Matrix((a, b, a.cross(b))).transposed()
def rot_between_frames(a0, b0, a1, b1):
    return (frame(a1, b1) @ frame(a0, b0).inverted()).to_quaternion()
SIDES = ('Left', 'Right')

class Rig:
    def __init__(self, arm, ground_z, top_z):
        self.arm = arm; B = arm.data.bones
        self.R = {b.name: b.matrix_local.to_quaternion() for b in B}
        self.H = {b.name: b.head_local.copy() for b in B}
        self.P = {b.name: (b.parent.name if b.parent else None) for b in B}
        self.order = []
        def walk(b):
            self.order.append(b.name)
            for c in b.children: walk(c)
        for b in B:
            if not b.parent: walk(b)
        self.g = ground_z; self.Ht = top_z - ground_z
        H = self.H
        self.Lg = (H['LeftLeg'] - H['LeftUpLeg']).length + (H['LeftFoot'] - H['LeftLeg']).length
        self.La = {s: (H[s + 'ForeArm'] - H[s + 'Arm']).length + (H[s + 'Hand'] - H[s + 'ForeArm']).length for s in SIDES}
        self.hasF = all(s + 'Fingers' in H for s in SIDES)
        self.spine = [n for n in ('Spine02', 'Spine01', 'Spine') if n in H]
        self.chest = self.spine[-1]
        self.TW = .65; self.TWMAX = 80; self.lastTw = {}; self.prevPsi = {}; self.PSIMAX = 80; self.PSIW = .25; self.WRMAX = 55; self.blades = {}
    def handdir(self, s):
        H = self.H; return ((H[s + 'Fingers'] if self.hasF else H[s + 'Hand'] + (H[s + 'Hand'] - H[s + 'ForeArm'])) - H[s + 'Hand']).normalized()
    def blade_rest(self, s):
        y = self.handdir(s); x = y.cross(F)
        if x.length < 1e-4: x = L.copy()
        x.normalize(); return x.cross(y).normalized(), y

    # ---- résolution d'une pose ----
    def solve(self, P):
        H, R = self.H, self.R; D = {}; W = {}
        Lg, Ht = self.Lg, self.Ht
        root = ch(P.get('root', (0, 0, 0))) * Lg
        D['Hips'] = rotq(P.get('hips', (0, 0, 0)))
        sp = P.get('spine', (0, 0, 0)); fr = {'Spine02': .25, 'Spine01': .35, 'Spine': .4}
        rel = {}
        for n in self.spine: rel[n] = rotq([v * fr.get(n, 1 / len(self.spine)) / (sum(fr.get(m, 1 / len(self.spine)) for m in self.spine)) for v in sp])
        if 'neck' in H: rel['neck'] = rotq(P.get('neck', (0, 0, 0)))
        if 'Head' in H: rel['Head'] = rotq(P.get('head', (0, 0, 0)))
        # FK du tronc
        def fk(n):
            p = self.P[n]
            if p is None or p not in W: W[n] = H[n] + root; return  # os « root » au-dessus du bassin (modèles du paquet)
            W[n] = W[p] + D[p] @ (H[n] - H[p])
            D[n] = D[p] @ rel[n] if n in rel else D[p]
        tronc = ['Hips'] + self.spine + [n for n in ('neck', 'Head', 'head_end', 'headfront') if n in H]
        for n in tronc: fk(n)
        chest = self.chest; Dc = D[chest]
        # clavicules (élévation automatique selon la hauteur de la main) puis bras en IK
        hands = {}
        for s in SIDES:
            sh = s + 'Shoulder'; W[sh] = W[self.P[sh]] + D[self.P[sh]] @ (H[sh] - H[self.P[sh]])
        def target_hand(s, spec):
            mode, v = spec[0], spec[1:]
            La = self.La[s]; Wsh = W[sh_of(s)]
            if mode == 's': return Wsh + Dc @ ch(v) * La
            if mode == 'sw': return Wsh + ch(v) * La
            if mode == 'w': return Vector((0, 0, self.g)) + ch(v) * Ht
            if mode == 'h': return W['Head'] + ch(v) * Ht
            raise ValueError(mode)
        def sh_of(s): return s + 'Arm'
        for s in SIDES:  # position provisoire de l'épaule (sans élévation)
            a = s + 'Arm'; W[a] = W[s + 'Shoulder'] + D[self.P[s + 'Shoulder']] @ (H[a] - H[s + 'Shoulder'])
        def arm(s, T, pole, blade=None, fing=None, wrist=None):
            sh = s + 'Shoulder'; a = s + 'Arm'; f = s + 'ForeArm'; h = s + 'Hand'
            # élévation de la clavicule : jusqu'à 22° quand la main monte au-dessus de l'épaule
            up = (T - W[a]).dot(U) / self.La[s]; el = max(0, min(1, up + .15)) * 22
            fw = max(0, min(1, (T - W[a]).dot(F) / self.La[s])) * 10
            ax = Vector((0, -1, 0)) if s == 'Left' else Vector((0, 1, 0))
            D[sh] = Dc @ Quaternion(ax, rad(el)) @ Quaternion(U if s == 'Left' else -U, rad(fw))
            W[sh] = W[self.P[sh]] + D[self.P[sh]] @ (H[sh] - H[self.P[sh]])
            W[a] = W[sh] + D[sh] @ (H[a] - H[sh])
            A = (H[f] - H[a]).length; Bl = (H[h] - H[f]).length
            S = W[a]; dv = T - S; d = max(1e-4, min(dv.length, (A + Bl) * .999)); n = dv.normalized()
            m0 = pole - n * pole.dot(n); m0 = m0.normalized() if m0.length > 1e-5 else n.orthogonal().normalized()
            ca = max(-1, min(1, (A * A + d * d - Bl * Bl) / (2 * A * d))); sa = math.sqrt(max(0, 1 - ca * ca))
            Tt = S + n * d
            nr = (H[h] - H[a]).normalized(); er = (H[f] - H[a]); mr = er - nr * er.dot(nr)
            mr = mr.normalized() if mr.length > 1e-4 else F.copy()
            Nr = mr.cross(nr)
            br, yr = self.blade_rest(s)
            Rc = yr.rotation_difference((H[h] - H[f]).normalized())  # poignet « droit » : main dans l'axe de l'avant-bras
            bt = ch(blade).normalized() if blade is not None else None
            def trial(psi):
                m = Quaternion(n, rad(psi)) @ m0
                E = S + n * A * ca + m * A * sa; Nt = m.cross(n)
                Da = rot_between_frames(H[f] - H[a], Nr, E - S, Nt); Df = rot_between_frames(H[h] - H[f], Nr, Tt - E, Nt)
                if bt is None: return 0, Da, Df, E, 0
                aw = (Tt - E).normalized(); c = Df @ Rc @ br; cp = c - aw * c.dot(aw); tp = bt - aw * bt.dot(aw); phi = 0
                if cp.length > 1e-3 and tp.length > 1e-3:
                    phi = math.atan2(cp.cross(tp).dot(aw), cp.dot(tp)); lim = rad(self.TWMAX); phi = max(-lim, min(lim, phi))
                    Df = Quaternion(aw, phi) @ Df
                sw = (Df @ Rc @ br).angle(bt)
                return math.degrees(abs(phi)) * .5 + math.degrees(sw) + abs(psi) * self.PSIW + abs(psi - self.prevPsi.get(s, psi)) * .3, Da, Df, E, phi
            best = None
            rng = range(-self.PSIMAX, self.PSIMAX + 1, 5) if bt is not None else [0]
            for psi in rng:
                r_ = trial(psi)
                if best is None or r_[0] < best[0][0]: best = (r_, psi)
            (cost, D[a], D[f], E, phi), psi = best; self.prevPsi[s] = psi; self.lastTw[s] = math.degrees(phi)
            W[f] = E; W[h] = Tt
            Cf = D[f]
            if bt is not None:
                if fing is not None:
                    hint = ch(fing).normalized(); yt = hint - bt * hint.dot(bt)
                    if yt.length < 1e-3: yt = (Cf @ yr); yt = yt - bt * yt.dot(bt)
                    yt.normalize()
                    D[h] = (Matrix((yt.cross(bt), yt, bt)).transposed() @ Matrix((yr.cross(br), yr, br)).transposed().inverted()).to_quaternion()
                else:
                    Cn = Cf @ Rc; c = Cn @ br; sw = c.rotation_difference(bt); ang_ = 2 * math.acos(max(-1, min(1, sw.w)))
                    if ang_ > rad(self.WRMAX): sw = Quaternion(sw.axis, rad(self.WRMAX))
                    D[h] = sw @ Cn
                self.blades[s] = D[h] @ br
            else:
                D[h] = Cf @ Rc.slerp(Quaternion(), .5) @ rotq(wrist or (0, 0, 0))
            if self.hasF:
                fn = s + 'Fingers'; W[fn] = W[h] + D[h] @ (H[fn] - H[h])
            return W[h]
        def pole_of(s, v):
            if v is None: v = (-.3, 1 if s == 'Left' else -1, -.6)
            return Dc @ ch(v)
        def evalT(s, spec):
            o = 'Right' if s == 'Left' else 'Left'
            if spec[0] == 'mix':
                Ta, ga = evalT(s, spec[1]); Tb, gb = evalT(s, spec[2]); w = max(0, min(1, spec[3]))
                return Ta.lerp(Tb, w), (ga if w < .5 else gb)
            if spec[0] == 'grip':
                bt = self.blades.get(o, ch(P['blade' + o[0]])).normalized(); return W[o + 'Hand'] + bt * spec[1] * self.Ht, tuple(Vector((-bt.y, bt.x, bt.z)))
            if spec[0] == 'o': return W[o + 'Hand'] + ch(spec[1:]) * self.Ht, None
            return target_hand(s, spec), None
        def uses_o(sp):
            return isinstance(sp, tuple) and (sp[0] == 'o' or (sp[0] == 'mix' and (uses_o(sp[1]) or uses_o(sp[2]))))
        self.blades = {}
        order_ = ('Left', 'Right') if uses_o(P.get('handR')) else ('Right', 'Left')
        for s in order_:
            spec = P.get('hand' + s[0])
            if spec is None: spec = ('s', .12, .12 if s == 'Left' else -.12, -.97)
            T, gb = evalT(s, spec)
            hands[s] = arm(s, T, pole_of(s, P.get('elbow' + s[0])), blade=gb if gb is not None else P.get('blade' + s[0]), fing=P.get('fing' + s[0]), wrist=P.get('wrist' + s[0]))
        # jambes en IK : chevilles plantées
        for s in SIDES:
            up = s + 'UpLeg'; lg = s + 'Leg'; ft = s + 'Foot'; toe = s + 'ToeBase'
            W[up] = W['Hips'] + D['Hips'] @ (H[up] - H['Hips'])
            off = P.get('foot' + s[0], (0, 0, 0))
            if P.get('feetrel'):  # pieds attachés au bassin (vol, roulade)
                T = W['Hips'] + D['Hips'] @ (H[ft] - H['Hips'] + ch(off) * Lg)
            else: T = H[ft] + ch(off) * Lg
            kp = P.get('knee' + s[0]); pole = (D['Hips'] if P.get('feetrel') else rotq((0, P.get('hips', (0, 0, 0))[1] * .6, 0))) @ ch(kp if kp else (1, .15 if s == 'Left' else -.15, 0))
            A = (H[lg] - H[up]).length; Bl = (H[ft] - H[lg]).length
            S = W[up]; dv = T - S; d = max(1e-4, min(dv.length, (A + Bl) * .9995)); n = dv.normalized()
            m = pole - n * pole.dot(n); m = m.normalized() if m.length > 1e-5 else F.copy()
            ca = max(-1, min(1, (A * A + d * d - Bl * Bl) / (2 * A * d))); sa = math.sqrt(max(0, 1 - ca * ca))
            E = S + n * A * ca + m * A * sa; Tt = S + n * d
            nr = (H[ft] - H[up]).normalized(); mr = F - nr * F.dot(nr); mr.normalize(); Nr = mr.cross(nr); Nt = m.cross(n)
            D[up] = rot_between_frames(H[lg] - H[up], Nr, E - S, Nt)
            D[lg] = rot_between_frames(H[ft] - H[lg], Nr, Tt - E, Nt)
            W[lg] = E; W[ft] = Tt
            fr_ = P.get('footrot' + s[0], (0, 0, 0))
            D[ft] = (D['Hips'] @ rotq(fr_)) if P.get('feetrel') else rotq((fr_[0], fr_[1] + P.get('hips', (0, 0, 0))[1] * .35, fr_[2] if len(fr_) > 2 else 0))
            if toe in H: D[toe] = D[ft] @ rotq((P.get('toe' + s[0], 0), 0, 0))
        # tous les autres os suivent leur parent
        for n in self.order:
            if n not in D: D[n] = D[self.P[n]] if self.P[n] else Quaternion()
        Q = {}
        for n in self.order:
            p = self.P[n]; Dp = D[p] if p else Quaternion()
            Q[n] = R[n].inverted() @ Dp.inverted() @ D[n] @ R[n]
        for s in SIDES:
            fn = s + 'Fingers'
            if fn in Q:  # flexion des doigts autour de l'axe du plan de la main
                c = P.get('curl' + s[0], 25)
                Q[fn] = Q[fn] @ Quaternion(Vector((1, 0, 0)), rad(c))
        loc = R['Hips'].inverted() @ root
        return Q, loc, W

# ---- interpolation des clés (Catmull-Rom, arrêts possibles) ----
def _vals(keys, name):
    out = []; last = None
    for k in keys:
        if name in k[1]: last = k[1][name]
        out.append(last)
    return out
def _num(x): return isinstance(x, (int, float))
def interp(keys, t, loop=False):
    ts = [k[0] for k in keys]; names = set(); [names.update(k[1].keys()) for k in keys]
    P = {}
    i = 0
    while i < len(ts) - 2 and t > ts[i + 1]: i += 1
    t0, t1 = ts[i], ts[i + 1]; u = 0 if t1 == t0 else max(0, min(1, (t - t0) / (t1 - t0)))
    stop1 = keys[i][1].get('_stop', False); stop2 = keys[i + 1][1].get('_stop', False)
    ease = keys[i + 1][1].get('_ease')
    if ease == 'out': u2 = 1 - (1 - u) ** 2.2
    elif ease == 'in': u2 = u ** 2.2
    else: u2 = None
    for nm in names:
        if nm.startswith('_'): continue
        vs = _vals(keys, nm)
        a, b = vs[i], vs[i + 1]
        if a is None: a = b
        if b is None: b = a
        if a is None: continue
        if isinstance(a, tuple) and a[0] == 'mix' and isinstance(b, tuple) and b[0] == 'mix':
            w = u2 if u2 is not None else u * u * (3 - 2 * u); P[nm] = ('mix', a[1], a[2], a[3] + (b[3] - a[3]) * w); continue
        if isinstance(a, bool) or isinstance(a, str) or (isinstance(a, tuple) and isinstance(a[0], str) and (not isinstance(b, tuple) or a[0] != b[0] or a[0] == 'grip')):
            if isinstance(a, tuple) and a[0] == 'grip' and isinstance(b, tuple) and b[0] == 'grip':
                P[nm] = ('grip', a[1] + (b[1] - a[1]) * (u2 if u2 is not None else u * u * (3 - 2 * u)))
            else: P[nm] = a if u < .5 else b
            continue
        pre = isinstance(a, tuple) and isinstance(a[0], str)
        A = list(a[1:] if pre else (a if isinstance(a, (tuple, list)) else [a])); Bv = list(b[1:] if pre else (b if isinstance(b, (tuple, list)) else [b]))
        if not _num(A[0]): P[nm] = a; continue
        dt = t1 - t0
        def tang(j):
            if j <= 0 or j >= len(keys) - 1 or keys[j][1].get('_stop'): return [0] * len(A)
            p0, p2 = vs[j - 1], vs[j + 1]
            if p0 is None or p2 is None: return [0] * len(A)
            p0 = list(p0[1:] if pre else (p0 if isinstance(p0, (tuple, list)) else [p0])); p2 = list(p2[1:] if pre else (p2 if isinstance(p2, (tuple, list)) else [p2]))
            if len(p0) != len(A) or len(p2) != len(A): return [0] * len(A)
            return [(p2[c] - p0[c]) / (ts[j + 1] - ts[j - 1]) for c in range(len(A))]
        m0, m1 = tang(i), tang(i + 1)
        if u2 is not None:
            R = [A[c] + (Bv[c] - A[c]) * u2 for c in range(len(A))]
        else:
            h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
            R = [h00 * A[c] + h10 * dt * m0[c] + h01 * Bv[c] + h11 * dt * m1[c] for c in range(len(A))]
        if pre: P[nm] = (a[0],) + tuple(R)
        elif isinstance(a, (tuple, list)): P[nm] = tuple(R)
        else: P[nm] = R[0]
    for k in keys[i + 1][1]:
        if k in ('feetrel',): P[k] = keys[i + 1][1][k] if u > .5 else keys[i][1].get(k, False)
    return P

LAG = {'head': .05, 'neck': .03}
DEF = {'root': (0, 0, 0), 'hips': (0, 0, 0), 'spine': (0, 0, 0), 'neck': (0, 0, 0), 'head': (0, 0, 0), 'footL': (0, 0, 0), 'footR': (0, 0, 0),
       'footrotL': (0, 0, 0), 'footrotR': (0, 0, 0), 'toeL': 0, 'toeR': 0, 'curlL': 25, 'curlR': 25, 'handR': ('s', .12, -.12, -.97), 'handL': ('s', .12, .12, -.97),
       'elbowR': (-.3, -1, -.6), 'elbowL': (-.3, 1, -.6), 'kneeL': (1, .15, 0), 'kneeR': (1, -.15, 0)}
def bake(rig, name, keys, step=1):
    names = set(); [names.update(k[1].keys()) for k in keys]
    k0 = dict(keys[0][1])
    for n in names:
        if n not in k0 and n in DEF:
            d = DEF[n]
            if n in ('handR', 'handL'):
                first = next(k[1][n] for k in keys if n in k[1])
                if first[0] == 'mix': d = ('mix', first[1], first[2], 0) if first[1] == d else first
            k0[n] = d
    keys = [(keys[0][0], k0)] + list(keys[1:])
    arm = rig.arm; T = keys[-1][0]
    act = bpy.data.actions.new(name); arm.animation_data_create(); arm.animation_data.action = act
    prev = {}
    nfr = int(round(T * FPS))
    for fi in range(0, nfr + 1, step):
        t = fi / FPS
        P = interp(keys, t)
        for ch_, lag in LAG.items():
            if ch_ in P: P[ch_] = interp(keys, max(0, t - lag)).get(ch_, P[ch_])
        Q, loc, W = rig.solve(P)
        for n, q in Q.items():
            pb = arm.pose.bones[n]; pb.rotation_mode = 'QUATERNION'
            if n in prev and prev[n].dot(q) < 0: q = -q
            prev[n] = q; pb.rotation_quaternion = q; pb.keyframe_insert('rotation_quaternion', frame=fi)
        pb = arm.pose.bones['Hips']; pb.location = loc; pb.keyframe_insert('location', frame=fi)
    for fc in act.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    return act
