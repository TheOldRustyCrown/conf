#!/data/data/com.termux/files/usr/bin/bash

apt update
apt upgrade -y
apt install nodejs-lts -y
apt install git -y
apt install nano -y
apt install openssh -y

termux-setup-storage

git config --global user.name "nucld"
git config --global user.email grimufa@gmail.com

# add remote rep
git remote add origin git@github.com:nucld/nucld.github.io.git

# ssh setup
ssh-keygen -t rsa
ssh -T git@github.com

# ssh-keygen -t rsa -b 4096 -C "grimufa@gmail.com" 
