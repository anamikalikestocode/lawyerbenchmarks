"""Parse Vals benchmark pages: extract the astro-island props holding per-model results."""
import re, html, json, glob, os, sys

def deser(v):
    # Astro prop serialisation: [type, value]; 0 = plain (recurse into dict), 1 = array
    if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
        t, x = v
        if t == 0:
            if isinstance(x, dict):
                return {k: deser(val) for k, val in x.items()}
            return x
        if t == 1:
            return [deser(i) for i in x]
        return x
    if isinstance(v, dict):
        return {k: deser(val) for k, val in v.items()}
    return v

def islands(path):
    h = open(path, encoding='utf-8', errors='ignore').read()
    out = []
    for m in re.finditer(r'<astro-island[^>]*?\sprops="([^"]*)"', h):
        raw = html.unescape(m.group(1))
        try:
            out.append(deser(json.loads(raw)))
        except Exception as e:
            pass
    return out, h

def find_key(obj, key, depth=0):
    """Yield every dict that has `key`."""
    if depth > 8: return
    if isinstance(obj, dict):
        if key in obj: yield obj
        for v in obj.values():
            yield from find_key(v, key, depth+1)
    elif isinstance(obj, list):
        for v in obj:
            yield from find_key(v, key, depth+1)

if __name__ == '__main__':
    os.makedirs('data/vals', exist_ok=True)
    summary = []
    for p in sorted(glob.glob('raw/vals/*.html')):
        slug = os.path.basename(p)[:-5]
        isl, h = islands(p)
        best = None
        for i in isl:
            for d in find_key(i, 'tasks'):
                t = d.get('tasks')
                if isinstance(t, dict) and 'overall' in t and isinstance(t['overall'], dict) and len(t['overall']) > 0:
                    if best is None or len(t['overall']) > len(best['tasks']['overall']):
                        best = d
        m = re.search(r'data-leader-summary[^>]*>\s*As of ([A-Za-z]+ \d+, \d{4})', h)
        asof = m.group(1) if m else None
        if best is None:
            summary.append((slug, 0, 0, asof, 'NO DATA')); continue
        json.dump({'slug': slug, 'as_of': asof, 'data': best}, open(f'data/vals/{slug}.json', 'w'))
        tasks = best['tasks']
        keys = [k for k in best.keys() if k != 'tasks']
        summary.append((slug, len(tasks['overall']), len(tasks), asof, ','.join(keys)[:80]))
    for s in summary: print(*s, sep=' | ')
