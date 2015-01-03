# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.hostname = "walter-test"
  # [todo] - import all dotfiles with single command/script
  # config.vm.provision "file", source: "~/dotfiles/zshrc",
  #                     destination: "~/.zshrc"
  # config.vm.provision "file", source: "~/dotfiles/zsh_aliases",
  #                     destination: "~/.zsh_aliases"
  config.vm.provision :shell, path: "bootstrap.sh"
end
