#!/bin/bash
# This script is meant to be run in the manylinux2014 docker container
# to build wheels.
set -euxo pipefail
PYTHON_VERSIONS="cp37-cp37m cp38-cp38 cp39-cp39"

wheeldir=$(mktemp -d)

for PYTHON_VERSION in $PYTHON_VERSIONS; do
	PYBIN="/opt/python/${PYTHON_VERSION}/bin"
    "${PYBIN}/pip" wheel /io/ --no-deps -w "$wheeldir"
done

# Bundle external shared libraries into the wheels
for whl in "$wheeldir"/*.whl; do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w "$wheeldir"
done

# fix wheel with our custom script
for whl in "$wheeldir"/*manylinux2014_x86_64.whl; do
	/opt/python/cp39-cp39/bin/python /io/python/fix_wheel.py "$whl" /io/dist
done


# run tests
for PYTHON_VERSION in $PYTHON_VERSIONS; do
	PYBIN="/opt/python/${PYTHON_VERSION}/bin"
    "${PYBIN}/pip" install 'protozfits[all]' -f /io/dist
    (cd "$HOME"; "${PYBIN}/python" -m pytest /io/python/)
done
