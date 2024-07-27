#!/bin/bash

# Définir le répertoire de sauvegarde
BACKUP_DIR="/home/ubuntu/backups"

# Créer un nom de dossier unique avec la date et l'heure
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M)"

# Créer le dossier de sauvegarde
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Copier les projets dans le dossier de sauvegarde
cp -r /home/ubuntu/emailfinder "$BACKUP_DIR/$BACKUP_NAME/"
cp -r /home/ubuntu/websitecrawl "$BACKUP_DIR/$BACKUP_NAME/"

# Supprimer les sauvegardes de plus de 24 heures
find "$BACKUP_DIR" -type d -mtime +1 -exec rm -rf {} +

# Ajouter une note dans le fichier README
echo "Sauvegarde créée le $(date)" >> "$BACKUP_DIR/README.txt"
