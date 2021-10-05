# Install general packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3.9 python3-pip
sudo apt autoclean -y
sudo apt autoremove -y

# Install miniconda
# wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
# sudo md5sum Miniconda3-latest-Linux-armv7l.sh
# sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh -b -p ~/miniconda3/
# export PATH="~/miniconda3/bin:$PATH"

# conda config --add channels rpi
# conda create -y --name my_root --clone=/home/pi/miniconda3
# source activate my_root
# conda install python=3.6

# Create env
# conda create -y --name c2l3play python=3.6
# source activate c2l3play

# Get project repository
cd ~/Desktop/
git clone https://github.com/numediart/ronde-nuit.git
cd ronde-nuit/

# Install python packages
pip install --upgrade setuptools
pip install --upgrade pip
pip install -r requirements.txt
