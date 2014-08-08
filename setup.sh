echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> .bashrc
apt-get -y update
apt-get -y install packaging-dev pkg-config python-dev libpango1.0-dev libglib2.0-dev libxml2-dev giflib-dbg libjpeg-dev libtiff-dev uthash-dev
apt-get -y install git
git clone https://github.com/fontforge/fontforge.git ff
cd ff
./bootstrap
./configure
make
sudo make install
cd ..
wget https://pypi.python.org/packages/source/t/tornado/tornado-4.0.tar.gz
tar xvzf tornado-4.0.tar.gz
cd tornado-4.0
python setup.py build
python setup.py install
cd ..
