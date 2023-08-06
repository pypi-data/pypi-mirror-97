'''
This script fixes missing patches to the library names and rpaths
after running `auditwheel repair`.

It should no longer be needed after this auditwheel issue is fixed:
https://github.com/pypa/auditwheel/issues/48
'''
import os
from zipfile import ZipFile, ZIP_DEFLATED
import subprocess as sp
import tempfile
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('inwheel')
parser.add_argument('outdir')


def zip_dir(zip_file, path):
    for root, _, files in os.walk(path):
        for file in files:
            file = os.path.join(root, file)
            zip_file.write(file, os.path.relpath(file, path))

def lib_name(lib):
    return Path(lib).stem.partition('.')[0].partition('-')[0]


def get_needed_libs(lib):
    result = sp.run(['readelf', '-d', str(lib)], stdout=sp.PIPE, encoding='utf-8')
    out = result.stdout

    libs = re.findall(r'\(NEEDED\)\s+Shared library: \[(.*)\]', out)
    return libs


def fix_wheel(inwheel, outdir):

    with tempfile.TemporaryDirectory(prefix='fix_wheel_') as tmpdir:
        tmpdir = Path(tmpdir)

        print('Extracting wheel')
        ZipFile(inwheel).extractall(path=tmpdir)

        libsdir = next(tmpdir.glob('*.libs'))
        package_name = libsdir.stem

        libs = [p.name for p in libsdir.glob('*.so*')]
        without_hash = [lib_name(lib) for lib in libs]
        vendored_libs = dict(zip(without_hash, libs))


        for lib in tmpdir.glob('**/*.so'):
            print('Patching ', lib)

            rpath = os.path.relpath(libsdir, lib.parent)
            print(rpath)

            rpath = f'$ORIGIN:$ORIGIN/{rpath}'
            print('Using RPATH', rpath)
            sp.run(['patchelf', '--force-rpath', '--set-rpath', rpath , str(lib)], check=True)

            needed_libs = get_needed_libs(lib)

            for needed in needed_libs:
                name = lib_name(needed)
                new = vendored_libs.get(name)
                if new and new != needed:
                    print(f'replacing {needed} with {new} in {lib.name}')
                    sp.run(['patchelf', '--remove-needed', needed, str(lib)], check=True)
                    sp.run(['patchelf', '--add-needed', new, str(lib)], check=True)


        outdir = Path(outdir)
        outdir.mkdir(exist_ok=True, parents=True)
        outwheel = outdir / Path(inwheel).name
        print(f'Writing fixed wheel to {outwheel}')
        with ZipFile(outwheel, 'w', compression=ZIP_DEFLATED, compresslevel=7) as zip_file:
            zip_dir(zip_file, tmpdir)





def main():
    args = parser.parse_args()
    fix_wheel(args.inwheel, args.outdir)


if __name__ == '__main__':
    main()
