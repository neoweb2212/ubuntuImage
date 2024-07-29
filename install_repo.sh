#!/bin/bash

# Variables
REPO_URL="https://github.com/neoweb2212/ubuntuImage.git"
REPO_DIR="/home/ubuntu/ubuntuImage"

# Cloner le dépôt GitHub
cd /home/ubuntu/
git clone $REPO_URL

# Accéder au répertoire cloné
cd $REPO_DIR

# Installer les paquets .deb si présents
for deb in *.deb; do
    if [ -f "$deb" ]; then
        echo "Installing $deb..."
        sudo dpkg -i "$deb"
    fi
done

# Corriger les dépendances manquantes
sudo apt --fix-broken install -y

# Exécuter des scripts d'installation si présents
for script in *.sh; do
    if [ -f "$script" ]; then
        echo "Executing $script..."
        chmod +x "$script"
        ./"$script"
    fi
done

