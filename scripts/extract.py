import os, subprocess, zipfile, re, json, glob, shutil

ROOT = '/home/workspace/Projects/npci-cl-evolution/data'
APKS = f'{ROOT}/apks'
EX = f'{ROOT}/extracted'
os.makedirs(EX, exist_ok=True)

def sh(cmd, timeout=600):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

def sample_name(fname):
    return re.sub(r'\.(apk|xapk)$', '', fname)

def find_base_apk(bundle_dir):
    apks = glob.glob(f'{bundle_dir}/*.apk')
    if not apks: return None
    # base apk = the one whose name is NOT config.*
    for a in apks:
        if not os.path.basename(a).startswith('config.'):
            return a
    return max(apks, key=os.path.getsize)

def analyze(sample, path):
    out = {'sample': sample, 'source_file': os.path.basename(path)}
    d = f'{EX}/{sample}'
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(f'{d}/raw', exist_ok=True)
    # extract
    if path.endswith('.xapk'):
        sh(f'unzip -oq "{path}" -d {d}/raw/bundle')
        base = find_base_apk(f'{d}/raw/bundle')
        out['bundle_files'] = [os.path.basename(x) for x in glob.glob(f'{d}/raw/bundle/*')]
    else:
        base = path
    if not base:
        out['error'] = 'no base apk found'
        return out
    sh(f'unzip -oq "{base}" -d {d}/raw/app')
    app = f'{d}/raw/app'
    out['base_apk'] = os.path.basename(base)
    # dexes
    dexes = sorted(glob.glob(f'{app}/classes*.dex'))
    out['dex_count'] = len(dexes)
    npci_dexes = []
    for dx in dexes:
        blob = open(dx, 'rb').read()
        if b'npci' in blob or b'NPCI' in blob:
            npci_dexes.append(dx)
    out['npci_dexes'] = [os.path.basename(x) for x in npci_dexes]
    # strings from npci dexes
    allstrings = []
    for dx in npci_dexes:
        r = sh(f'strings -a -n 4 "{dx}"')
        allstrings.append(r.stdout)
    st = '\n'.join(allstrings)
    open(f'{d}/npci_dex_strings.txt', 'w').write(st)
    # package inventory
    pkgs = set(re.findall(r'L(?:[a-zA-Z0-9_/$-]*?)npci[a-zA-Z0-9_/$.-]*;', st))
    pkgs = sorted(p[1:-1].replace('/', '.') for p in pkgs)
    out['npci_classes'] = pkgs
    # version-like strings
    vstr = sorted(set(re.findall(r'\b\d+\.\d+(?:-v\d+\.\d+)?\b', st)))
    out['version_like_strings'] = vstr[:60]
    # lite/CL markers
    for marker, pat in [
        ('lite', r'[Uu][Pp][Ii][_. ]?[Ll]ite|LITE'),
        ('cl', r'CommonLibrary|commonlibrary|CL_VERSION|pinactivity'),
    ]:
        out[f'marker_{marker}'] = len(re.findall(pat, st))
    # native libs
    libs = sorted(glob.glob(f'{app}/lib/arm64-v8a/*.so')) or sorted(glob.glob(f'{app}/lib/armeabi-v7a/*.so'))
    out['lib_count'] = len(libs)
    cl_libs = []
    for lb in libs:
        b = os.path.basename(lb).lower()
        if any(k in b for k in ['secure', 'npci', 'upi', 'pin', 'cl']):
            cl_libs.append(os.path.basename(lb))
    out['cl_candidate_libs'] = cl_libs
    sostrings = {}
    for lb in libs:
        b = os.path.basename(lb).lower()
        if any(k in b for k in ['secure', 'npci', 'upi', 'pin', 'cl', 'native-lib']):
            r = sh(f'strings -a -n 5 "{lb}"')
            sostrings[os.path.basename(lb)] = r.stdout
    if sostrings:
        open(f'{d}/so_strings.txt', 'w').write('\n\n===== '.join(f'{k} =====\n{v}' for k, v in sostrings.items()))
        joined = '\n'.join(sostrings.values())
        out['so_version_like'] = sorted(set(re.findall(r'\b\d+\.\d+(?:-v\d+\.\d+)?\b', joined)))[:40]
    # try jadx single-class for CLConstants
    jadx_out = f'{d}/jadx'
    os.makedirs(jadx_out, exist_ok=True)
    for cls in ['org.npci.upi.security.pinactivitycomponent.CLConstants',
                'in.org.npci.commonlibrary.CLConstants']:
        target = f'{jadx_out}/{cls}.java'
        r = sh(f'jadx --single-class {cls} --single-class-output "{target}" "{npci_dexes[0] if npci_dexes else dexes[0]}" 2>/dev/null', timeout=900)
        if os.path.exists(target):
            out['clconstants_class'] = cls
            break
    return out

samples = sorted(os.listdir(APKS))
results = {}
for f in samples:
    if not f.endswith(('.apk', '.xapk')): continue
    s = sample_name(f)
    print(f'=== {s} ===', flush=True)
    try:
        results[s] = analyze(s, f'{APKS}/{f}')
    except Exception as e:
        results[s] = {'sample': s, 'error': str(e)}
    print(json.dumps({k: v for k, v in results[s].items() if k not in ('npci_classes', 'version_like_strings')}, indent=1)[:900], flush=True)

json.dump(results, open(f'{EX}/_analysis_index.json', 'w'), indent=1)
print('DONE', len(results))
