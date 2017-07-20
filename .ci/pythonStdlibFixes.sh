if $( python -c "import sys;sys.exit(int(not (sys.version_info < (3, 5)) ))" ); then curl -O https://raw.githubusercontent.com/python/cpython/3.6/Lib/typing.py; fi;
if $( python -c "import sys;sys.exit(int(not (sys.version_info < (3, 6)) ))" ); then curl -O https://raw.githubusercontent.com/python/cpython/3.7/Lib/enum.py; fi;
