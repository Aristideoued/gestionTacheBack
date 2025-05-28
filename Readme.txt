# Projet Flask avec PostgreSQL

Ce projet est une application web développée avec le framework Flask et utilise PostgreSQL comme base de données. Ce guide vous aidera à configurer et lancer le projet en local.

---

## 🔧 Prérequis

- Python 3.8 ou supérieur
- PostgreSQL
- `git` (pour cloner le projet)

---

## 📦 Installation


2. Créer et activer un environnement virtuel

Sous Linux/macOS
bash

Copier le code:
python3 -m venv venv
source venv/bin/activate

Sous Windows
cmd
Copier le code:
python -m venv venv
venv\Scripts\activate

3. Installer les dépendances
bash
Copier le code:
pip install -r requirements.txt

🐘 Configuration de PostgreSQL
1. Assurez-vous que PostgreSQL est installé et en cours d'exécution.
2. Créez une base de données pour le projet :
bash
Copier le code:
createdb nom_de_votre_base
ou depuis pgAdmin

3. Modifiez les variables d'environnement ou le fichier .env (si utilisé) pour configurer la connexion :
bash
Copier le code
DATABASE_URL=postgresql://postgres:2885351@localhost:5432/jofesig
💡 Exemple :DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myflaskdb

⚙️ Initialisation de la base de données
Exécutez les commandes suivantes pour créer les tables et insérer le compte administrateur par défaut :
bash
Copier le code:
flask db upgrade

Lancement de l'application
bash
Copier le code
flask run
L’application sera disponible sur http://localhost:5000

👤 Compte administrateur par défaut
Lors de la première initialisation, un compte administrateur est automatiquement créé avec les identifiants suivants :
* Nom d'utilisateur : admin
* Mot de passe : admin
🔐 Pensez à modifier ce mot de passe dans un environnement de production.