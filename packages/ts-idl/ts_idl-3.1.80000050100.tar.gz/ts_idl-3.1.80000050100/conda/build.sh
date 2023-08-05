pip install -e .

cp -v /opt/lsst/ts_sal/idl/*idl `python -c 'from lsst.ts import idl; print(idl.get_idl_dir())'`

python setup.py sdist
cd dist
pip install *.tar.gz
