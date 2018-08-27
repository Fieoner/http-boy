#!/bin/bash

if [ ! $UID -eq 0 ]
then
	echo "script must be run as root"
	exit 1
fi

apt update
apt -y install git pypy pypy-dev virtualenv libsdl2-dev libjpeg-dev

virtualenv . -p `which pypy`
source ./bin/activate

pip install git+https://bitbucket.org/pypy/numpy.git
pip install git+https://github.com/marcusva/py-sdl2.git
pip install imageio
