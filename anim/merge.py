# Remplace dans un GLB d'animations existant (paquet anim_*) les clips régénérés par gen.py, os par os (par nom).
# Usage : python3 merge.py anim_ancien.glb anim_nouveaux_clips.glb sortie.glb
# 0.4.1 : sert à refaire le combo de l'épée sans régénérer tous les autres clips. Le squelette source de gen.py doit être
# le GLB d'animations d'origine (axes Z-haut, os « Fingers ») et non le modèle du paquet corps_* (axes Y-haut, doigts détaillés).
import sys
from compact import load, save
def merge(ancien, nouveau, sortie):
    jo, bo = load(ancien); jn, bn = load(nouveau)
    noms = {a['name'] for a in jn['animations']}
    nom_noeud = {i: n.get('name') for i, n in enumerate(jn['nodes'])}; idx_old = {n.get('name'): i for i, n in enumerate(jo['nodes'])}
    jo['animations'] = [a for a in jo['animations'] if a['name'] not in noms]
    base = bytearray(bo)
    while len(base) % 4: base.append(0)
    off = len(base); base += bn; nv = len(jo['bufferViews'])
    for v in jn['bufferViews']:
        v = dict(v); v['buffer'] = 0; v['byteOffset'] = v.get('byteOffset', 0) + off; jo['bufferViews'].append(v)
    na = len(jo['accessors'])
    for ac in jn['accessors']:
        ac = dict(ac)
        if 'bufferView' in ac: ac['bufferView'] += nv
        jo['accessors'].append(ac)
    manque = set()
    for a in jn['animations']:
        ch = []
        for c in a['channels']:
            nm = nom_noeud[c['target']['node']]
            if nm not in idx_old: manque.add(nm); continue
            ch.append({'sampler': c['sampler'], 'target': {'node': idx_old[nm], 'path': c['target']['path']}})
        smp = [{'input': s['input'] + na, 'output': s['output'] + na, 'interpolation': s.get('interpolation', 'LINEAR')} for s in a['samplers']]
        jo['animations'].append({'name': a['name'], 'channels': ch, 'samplers': smp})
    jo['buffers'] = [{'byteLength': len(base)}]
    import tempfile, os
    t = tempfile.mktemp(suffix='.glb'); save(t, jo, bytes(base))
    from compact import compact
    compact(t, sortie); os.remove(t)
    return sorted(manque)
if __name__ == '__main__':
    print('MERGE', sys.argv[3], 'os absents :', merge(*sys.argv[1:4]))
