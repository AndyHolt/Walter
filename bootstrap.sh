# install necessary software
echo "installing software"
apt-get -qq update
apt-get -y install zsh git

# get dotfiles from github
# echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
# git clone git@github.com:AndyHolt/dotfiles.git dotfiles
git clone --recursive https://github.com/AndyHolt/dotfiles.git dotfiles
exec "/home/vagrant/dotfiles/bootstrap.sh" "vagrant"

# change shell to zsh
chsh -s /bin/zsh vagrant
