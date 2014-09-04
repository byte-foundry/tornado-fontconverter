echo "#####     CREATING .BASHRC FILE AND EDITING IT WITH LIBRAIRIES     #####"
touch ~/.bashrc && chmod 777 ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> .bashrc
source ~/.bashrc && echo "source bashrc complete"
echo "#####     UPDATING APT-GET     #####"
apt-get -y update
echo "#####     INSTALLING GIT...    #####"
apt-get -y install git
echo "#####     INSTALLING NODEJS & NPM...     #####"
apt-get -y update
apt-get install -y python-software-properties
add-apt-repository ppa:chris-lea/node.js
apt-get -y update
apt-get -y install nodejs
echo "#####     INSTALLING PM2...     #####"
sudo npm install pm2 -g --unsafe-perm
echo "#####     INSTALLING MAKE...     #####"
apt-get -y install make
echo "#####     UPDATING APT-GET     #####"
apt-get -y update
echo "#####     INSTALLING DEPENDENCIES FOR FONTFORGE...    #####"
apt-get -y install packaging-dev pkg-config python-dev libpango1.0-dev libglib2.0-dev libxml2-dev giflib-dbg libjpeg-dev libtiff-dev uthash-dev
echo "#####     INSTALLING FONTFORGE FROM SOURCES...    #####"
git clone https://github.com/fontforge/fontforge.git ff
cd ff
./bootstrap
./configure
make
make install
cd ..
echo "#####     DOWNLOADING PIP...    #####"
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
echo "#####     INSTALLING TORNADO & BOTO FROM PIP...     #####"
pip install tornado
pip install boto
pm2 start /home/vagrant/main.py -x --interpreter python
