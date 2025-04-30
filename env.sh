
module load PrgEnv-gnu

PY_EXEC=/opt/cray/pe/python/3.9.13.1/bin/python

export PY_WF_ROOT=${HOME/home/work}/.py_wf
mkdir -p $PY_WF_ROOT
if [ ! -d  "$PY_WF_ROOT/io_env" ]; then
    $PY_EXEC -m venv "$PY_WF_ROOT/io_env"
    $PY_EXEC -m pip install pip --upgrade
    $PY_EXEC -m pip install -r requirements.txt
fi

source "$PY_WF_ROOT/io_env/bin/activate"

export PYTHONPATH=$(pwd):$PYTHONPATH