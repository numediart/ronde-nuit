# Install general packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3.7 python-pip
sudo apt autoclean -y
sudo apt autoremove -y

# Get project repository
cd ~/Desktop/
git clone https://github.com/numediart/ronde-nuit.git
cd ronde-nuit/

# Install python packages
pip install -r requirements.txt