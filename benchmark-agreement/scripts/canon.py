"""Map each source's model label to one canonical model key. Effort settings are kept separately."""
import re, json
EFF = ['xhigh','max','high','medium','low','auto']
# same model, different label at different publishers
ALIAS = {'reflection-beam':'beam-1-0','tencent-hy4':'hy4','nemotron-3-5-super-vl':'nemotron-3-5-super-vl-120b-a12b'}
def canon(s):
    s = s.lower().strip()
    s = s.split('/')[-1]
    s = re.sub(r'\(.*?\)', '', s)                      # drop "(Max, Default Fallback)"
    s = s.replace('responses','').replace('_','-').replace(' ','-').replace('.','-')
    s = re.sub(r'^claude-', '', s)
    s = re.sub(r'-(internal|preview|default-fallback|fallback)$', '', s) if not s.endswith('pro-preview') else s
    toks = [t for t in s.split('-') if t]
    toks = [t for t in toks if t not in EFF]
    s = '-'.join(toks)
    s = re.sub(r'-(\d{4}|\d{2}-\d{2})$', '', s)        # date stamps: -1017, -08-13
    s = re.sub(r'^(muse-wonder)-1-0$', r'\1', s)
    s = s.replace('m3p1','m3-1').replace('qwen3-8','qwen-3-8').replace('qwen-3-8-max','qwen-3-8-max')
    s = re.sub(r'^beam(-1-0)?$', 'beam-1-0', s)
    s = re.sub(r'^gpt-5-6-sol-pro$', 'gpt-5-6-sol', s)
    return ALIAS.get(s, s)
if __name__ == '__main__':
    import glob, os
    seen = {}
    def add(src, label, extra=''):
        seen.setdefault(canon(label), []).append(f'{src}:{label}{extra}')
    for m in json.load(open('raw/vals_views/hlab.json'))['tasks']['overall']: add('valsLAB', m)
    for m in json.load(open('raw/vals_views/legal_research.json'))['tasks']['overall']: add('valsLR', m)
    for r in json.load(open('raw/aa/harvey_lab_aa_v1_1.json'))['rows']: add('aaLAB', r['aa_model_slug'], f"[{r.get('reasoning_setting')}]")
    for r in json.load(open('raw/other/mercor_apex_agents.json'))['rows']: add('apex', r['model_id'], f"[{r.get('reasoning_setting')}]")
    for r in json.load(open('raw/other/legora_bar_2026-10.json'))['rows']: add('legora', r['model_id'])
    for k in sorted(seen):
        srcs = sorted(set(x.split(':')[0] for x in seen[k]))
        if len(srcs) >= 2 or any(s in ('legora','aaLAB') for s in srcs): print(f"{k:28} {len(srcs)} | " + ' ; '.join(seen[k]))
