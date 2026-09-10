import os
import subprocess
import sys
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GEN_SCRIPT = os.path.join(ROOT_DIR, 'github-profile-3d-contrib-main', 'github-profile-3d-contrib-main', 'generate_local.js')
OUT_DIR = os.path.join(ROOT_DIR, 'profile-3d-contrib')
OUT_FILE = os.path.join(OUT_DIR, 'profile-gitblock.svg')
ROOT_OUT_FILE = os.path.join(ROOT_DIR, 'profile-gitblock.svg')

def main():
    print('Generating 3D GitBlock contribution graph...')
    if not os.path.exists(GEN_SCRIPT):
        print(f'Generator script not found at {GEN_SCRIPT}')
        return 1

    proc = subprocess.run(['node', GEN_SCRIPT], cwd=os.path.dirname(GEN_SCRIPT), capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)

    local_svg = os.path.join(os.path.dirname(GEN_SCRIPT), 'profile-3d-contrib', 'profile-gitblock.svg')
    if os.path.exists(local_svg):
        os.makedirs(OUT_DIR, exist_ok=True)
        shutil.copyfile(local_svg, OUT_FILE)
        shutil.copyfile(local_svg, ROOT_OUT_FILE)
        print('Successfully generated:')
        print(f' - {OUT_FILE}')
        print(f' - {ROOT_OUT_FILE}')
        return 0
    else:
        print('Error: profile-gitblock.svg was not created.')
        return 1

if __name__ == '__main__':
    sys.exit(main())
