## Sources :
## https://www.anegron.site/2020/06/18/how-to-install-conda-and-docker-on-your-raspberry-pi/

# Install general packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y net-tools openssh-server git python3.9 python3-pip
sudo apt autoclean -y
sudo apt autoremove -y

# Install miniconda
#wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-aarch64.sh
sudo md5sum Miniconda3-py39_4.9.2-Linux-aarch64.sh
#sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh -b -p ~/miniconda3/
sudo /bin/bash Miniconda3-py39_4.9.2-Linux-aarch64.sh -b -p ~/miniconda3/
sudo echo "export PATH=\"/home/pi/miniconda3/bin:$PATH\"" >> .bashrc
#export PATH="~/miniconda3/bin:$PATH"


# conda config --add channels rpi
# conda create -y --name my_root --clone=/home/pi/miniconda3
# source activate my_root
# conda install python=3.6

# Create env
conda create -y --name ronde python=3.9
conda init bash
source activate ronde

# Get project repository
#cd ~/Desktop/
#git clone https://github.com/numediart/ronde-nuit.git
#cd ronde-nuit/

# Install python packages
#pip install --upgrade setuptools
#pip install --upgrade pip
#pip install -r requirements.txt
