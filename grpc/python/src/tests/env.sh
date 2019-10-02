
source /auto/cafy/cafykit/cafy-exec/bin/activate

WS_ROOT=/ws/arhashem-sjc
CAFY_ROOT=/ws/arhashem-sjc/cafy
CAFYKIT_ROOT=$CAFY_ROOT/cafykit
CAFYAP_ROOT=$CAFY_ROOT/cafyap
export ARCHIVE_DIR=$PWD
export GIT_REPO=$CAFYKIT_ROOT
export PYTHONPATH="$GIT_REPO/lib:~/.local/lib/python3.6/site-packages"
export CAFYAP_REPO=$CAFYAP_ROOT
