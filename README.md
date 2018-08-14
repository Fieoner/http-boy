Installation
=====================

Ubuntu has some problems installing PyPy in parallel with the system version of CPython. Therefore, we will install the PyPy version of NumPy and PySDL2 in a virtualenv.

    sudo apt update
    sudo apt install git pypy pypy-dev virtualenv libsdl2-dev

Now move to the `PyBoy/Source` directory before creating the virtual environment:

    virtualenv . -p `which pypy`
    source ./bin/activate

    pip install git+https://bitbucket.org/pypy/numpy.git
    pip install git+https://github.com/marcusva/py-sdl2.git
