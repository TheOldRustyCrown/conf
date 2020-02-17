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
git config --global core.editor nano

mkdir dev
cd dev

npm init -y
git init

git remote add origin git@github.com:nucld/nucld.github.io.git
ssh-keygen -t rsa -b 4096 -C "grimufa@gmail.com" 
ssh -T git@github.com
