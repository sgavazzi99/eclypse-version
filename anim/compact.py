# Allège un GLB d'animations : ne garde que les rotations (et la translation du bassin), reconstruit le binaire.
import json, struct, sys
def load(f):
    b = open(f, 'rb').read(); n = struct.unpack('<I', b[12:16])[0]; j = json.loads(b[20:20 + n])
    o = 20 + n; bl = struct.unpack('<I', b[o:o + 4])[0]; return j, b[o + 8:o + 8 + bl]
def save(f, j, bin_):
    js = json.dumps(j, separators=(',', ':')).encode(); js += b' ' * ((4 - len(js) % 4) % 4); bin_ += b'\0' * ((4 - len(bin_) % 4) % 4)
    out = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bin_)) + struct.pack('<II', len(js), 0x4E4F534A) + js + struct.pack('<II', len(bin_), 0x004E4942) + bin_
    open(f, 'wb').write(out)
def compact(src, dst, keep_trans=('Hips',)):
    j, b = load(src); nodes = j['nodes']
    for a in j['animations']:
        ch = []
        for c in a['channels']:
            p = c['target']['path']; nm = nodes[c['target']['node']].get('name')
            if p == 'rotation' or (p == 'translation' and nm in keep_trans): ch.append(c)
        used = sorted(set(c['sampler'] for c in ch)); remap = {s: i for i, s in enumerate(used)}
        a['samplers'] = [a['samplers'][s] for s in used]
        for c in ch: c['sampler'] = remap[c['sampler']]
        a['channels'] = ch
    acc_used = set()
    for a in j['animations']:
        for s in a['samplers']: acc_used.update((s['input'], s['output']))
    for s in j.get('skins', []):
        if 'inverseBindMatrices' in s: acc_used.add(s['inverseBindMatrices'])
    acc_used = sorted(acc_used); amap = {}; newacc = []; views = []; nb = bytearray()
    CS = {5126: 4, 5123: 2, 5125: 4, 5121: 1}; NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}
    for ai in acc_used:
        ac = dict(j['accessors'][ai]); bv = j['bufferViews'][ac['bufferView']]
        size = CS[ac['componentType']] * NC[ac['type']] * ac['count']; st = bv.get('byteOffset', 0) + ac.get('byteOffset', 0)
        while len(nb) % 4: nb.append(0)
        views.append({'buffer': 0, 'byteOffset': len(nb), 'byteLength': size}); nb += b[st:st + size]
        ac['bufferView'] = len(views) - 1; ac.pop('byteOffset', None); amap[ai] = len(newacc); newacc.append(ac)
    for a in j['animations']:
        for s in a['samplers']: s['input'] = amap[s['input']]; s['output'] = amap[s['output']]
    for s in j.get('skins', []):
        if 'inverseBindMatrices' in s: s['inverseBindMatrices'] = amap[s['inverseBindMatrices']]
    j['accessors'] = newacc; j['bufferViews'] = views; j['buffers'] = [{'byteLength': len(nb)}]
    save(dst, j, bytes(nb))
if __name__ == '__main__':
    compact(sys.argv[1], sys.argv[2])
