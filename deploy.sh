#!/bin/bash

# Définir le répertoire de déploiement
DEPLOY_DIR="./github_actions/rikabot"

# Créer le répertoire s'il n'existe pas
mkdir -p $DEPLOY_DIR

# Aller au répertoire de déploiement
cd $DEPLOY_DIR

# Initialiser un dépôt Git - si le répertoire n'est pas déjà un dépôt Git
git init
git remote set-url origin git@github.com:ToyHugs/rika-bot-public.git


# Mettre à jour le dépôt et installer les dépendances
git fetch origin
git reset --hard origin/main

# Effectuer des actions spécifiques de déploiement
# Par exemple, redémarrer une application

# Recharger les variables d'environnement
source env-export.sh

# Force le redémarrage des conteneurs
docker-compose -f compose.yaml down

# Redémarre les conteneurs
docker-compose -f compose.yaml up -d --build