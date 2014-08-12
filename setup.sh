echo "#####     CREATING .BASHRC FILE AND EDITING IT WITH LIBRAIRIES     #####"
touch .bashrc && chmod 777 .bashrc
echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> .bashrc
source .bashrc && echo "source bashrc complete"
echo "#####     UPDATING APT-GET     #####"
apt-get -y update
echo "#####     INSTALLING GIT...    #####"
apt-get -y install git
echo "#####     INSTALLING NODEJS...     #####"
apt-get -y install nodejs
ln -s /usr/bin/nodejs /usr/bin/node
echo "#####     INSTALLING MAKE...     #####"
apt-get -y install make
echo "#####     INSTALLING NPM FROM GITHUB...     #####"
git clone https://github.com/npm/npm.git
cd npm
sudo make
sudo make install
cd ..
echo "#####     INSTALLING PM2...    #####"
sudo npm install pm2@latest -g
echo "#####     UPDATING APT-GET     #####"
apt-get -y update
echo "#####     INSTALLING DEPENDENCIES FOR FONTFORGE...    #####"
apt-get -y install packaging-dev pkg-config python-dev libpango1.0-dev libglib2.0-dev libxml2-dev giflib-dbg libjpeg-dev libtiff-dev uthash-dev
echo "#####     INSTALLING FONTFORGE FROM SOURCES...    #####"
git clone https://github.com/fontforge/fontforge.git ff
cd ff
./bootstrap
./configure
sudo make
sudo make install
cd ..
echo "#####     INSTALLING TORNADO FROM PIP...    #####"
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install tornado
echo "#####     LAUNCHING PM2 START...    #####"
pm2 start /home/bill/py-fontconv.py -x --interpreter python
