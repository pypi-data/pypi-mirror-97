#!/bin/bash
set -ex

curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain stable -y
export PATH="$HOME/.cargo/bin:$PATH"

for PYBIN in /opt/python/cp{36-cp36m,37-cp37m,38-cp38,39-cp39}/bin; do
    export PYTHON_SYS_EXECUTABLE="$PYBIN/python"

    "${PYBIN}/pip" install -U setuptools wheel setuptools-rust
    "${PYBIN}/python" setup.py bdist_wheel
    rm -r build/lib
done

for whl in dist/*.whl; do
    auditwheel repair "$whl" -w dist/
    rm $whl
done
