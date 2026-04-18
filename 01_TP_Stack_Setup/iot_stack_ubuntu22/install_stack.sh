#!/bin/bash

set -e

echo "⏳ Waiting for apt to be ready..."

while sudo lsof /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
  sleep 2
done

ROLE=$1

echo "======================================"
echo "🚀 Provisioning role: $ROLE"
echo "======================================"

sudo apt-get update -y

case $ROLE in

  # =========================
  # 🧠 ANSIBLE SERVER
  # =========================
  ansible)
    echo "📦 Installing Ansible..."

    ENABLE_ZSH=${ENABLE_ZSH:-false}
    VERSION_STRING="2.17.14-1ppa~jammy"

    # Common packages
    sudo apt-get install -y python3 python3-pip git curl wget
    sudo apt-get install -y software-properties-common

    # Add Ansible repo
    sudo add-apt-repository --yes --update ppa:ansible/ansible

    # Install Ansible (pinned version)
    sudo apt-get install -y ansible-core=$VERSION_STRING

    # Useful for automation
    sudo apt-get install -y sshpass

    ansible --version

    # =========================
    # 💡 Optional ZSH setup
    # =========================
    if [[ !(-z "$ENABLE_ZSH") && ($ENABLE_ZSH == "true") ]]; then
        echo "💻 Installing ZSH environment..."

        sudo apt-get install -y zsh git

        echo "vagrant" | chsh -s /bin/zsh vagrant

        su - vagrant -c 'echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'

        su - vagrant -c "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"

        sed -i 's/^plugins=/#&/' /home/vagrant/.zshrc

        echo "plugins=(git colored-man-pages aliases copyfile copypath zsh-syntax-highlighting jsontools)" >> /home/vagrant/.zshrc

        sed -i "s/^ZSH_THEME=.*/ZSH_THEME='agnoster'/g" /home/vagrant/.zshrc

    else
        echo "ℹ️ ZSH not enabled"
    fi

    ;;

  # =========================
  #  OPC UA SIMULATOR
  # =========================
  opcua_plc_simulator)
    echo "🐍 Installing Python3..."

    sudo apt-get install -y python3 python3-pip

    python3 --version
    pip3 --version
    ;;

  # =========================
  # ⚙️ EDGE GATEWAY (DOCKER)
  # =========================
  edge)
    echo "🐳 Installing Docker..."

    VERSION_STRING="5:25.0.3-1~ubuntu.22.04~jammy"
    ENABLE_ZSH=${ENABLE_ZSH:-false}

    sudo apt-get install -y ca-certificates curl

    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y

    sudo apt-get install -y \
      docker-ce=$VERSION_STRING \
      docker-ce-cli=$VERSION_STRING \
      containerd.io \
      docker-buildx-plugin \
      docker-compose-plugin

    sudo systemctl start docker
    sudo systemctl enable docker

    sudo usermod -aG docker vagrant

    echo '1' | sudo tee /proc/sys/net/bridge/bridge-nf-call-iptables > /dev/null

    docker --version

    # =========================
    # 💡 Optional ZSH setup
    # =========================
    if [[ !(-z "$ENABLE_ZSH") && ($ENABLE_ZSH == "true") ]]; then
        echo "💻 Installing ZSH environment..."

        sudo apt-get install -y zsh git

        echo "vagrant" | chsh -s /bin/zsh vagrant

        su - vagrant -c 'echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'

        su - vagrant -c "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"

        sed -i 's/^plugins=/#&/' /home/vagrant/.zshrc

        echo "plugins=(git docker docker-compose colored-man-pages aliases copyfile copypath dotenv zsh-syntax-highlighting jsontools)" >> /home/vagrant/.zshrc

        sed -i "s/^ZSH_THEME=.*/ZSH_THEME='agnoster'/g" /home/vagrant/.zshrc

    else
        echo "ℹ️ ZSH not enabled"
    fi

    ;;

  # =========================
  # ❌ UNKNOWN ROLE
  # =========================
  *)
    echo "❌ Unknown role: $ROLE"
    exit 1
    ;;

esac

# =========================
# 🌐 Show IP
# =========================
IP=$(ip -f inet addr show enp0s8 | sed -En -e 's/.*inet ([0-9.]+).*/\1/p')
echo "🌐 Machine IP Address: $IP"

echo "✅ Provisioning completed for $ROLE"