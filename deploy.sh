#!/bin/bash

# Définir le répertoire de déploiement
DEPLOY_DIR="./github_actions/rikabot"

# Créer le répertoire s'il n'existe pas
mkdir -p $DEPLOY_DIR

# Aller au répertoire de déploiement
cd $DEPLOY_DIR

# Si le répertoire n'est pas un dépôt Git, initialiser un dépôt
if [ ! -d ".git" ]; then
  git init
  git remote add origin git@github.com:your_username/your_repository.git
fi

# Mettre à jour le dépôt et installer les dépendances
git fetch origin
git reset --hard origin/main

# Effectuer des actions spécifiques de déploiement
# Par exemple, redémarrer une application

# Recharger les variables d'environnement
source env-export.sh

# Force le redémarrage des conteneurs
docker-compose -f docker-compose.yml down

# Redémarre les conteneurs
docker-compose -f docker-compose.yml up -d --build