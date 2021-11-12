## Sources :
## https://www.anegron.site/2020/06/18/how-to-install-conda-and-docker-on-your-raspberry-pi/

# Install general packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y net-tools openssh-server git python3.9 python3-pip
sudo apt autoclean -y
sudo apt autoremove -y


# Get project repository
cd ~/Desktop/
git clone https://github.com/numediart/ronde-nuit.git
cd ronde-nuit/

# Install python packages
pip install --upgrade setuptools
pip install --upgrade pip
pip install -r requirements.txt
