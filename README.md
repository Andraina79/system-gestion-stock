# Système de Gestion de Stock Commercial

## Description
Système complet de gestion d'inventaire en français pour petites et moyennes entreprises (PME), développé avec Flask et Python.

## Fonctionnalités
- ✅ Gestion complète des produits (ajout, modification, suppression)
- ✅ Suivi des mouvements de stock (entrées, sorties, ajustements)
- ✅ Alertes automatiques pour stock faible/critique
- ✅ Tableau de bord avec statistiques et graphiques
- ✅ Interface responsive avec thème sombre Bootstrap
- ✅ Recherche et filtrage avancés
- ✅ Export des données

## Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation locale
1. Téléchargez tous les fichiers du projet
2. Installez les dépendances :
```bash
pip install flask flask-sqlalchemy gunicorn email-validator psycopg2-binary
```

3. Configurez les variables d'environnement :
```bash
export SESSION_SECRET="votre-cle-secrete-ici"
```

4. Lancez l'application :
```bash
python main.py
```

5. Ouvrez votre navigateur sur : http://localhost:5000

### Déploiement sur serveur web

#### Option 1: Avec Gunicorn (recommandé)
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

#### Option 2: Hébergement gratuit
- **Heroku** : Suivez le guide d'installation Flask sur Heroku
- **Railway** : Connectez votre repository GitHub
- **Render** : Déployez directement depuis GitHub

### Configuration pour production
1. Changez la clé secrète dans les variables d'environnement
2. Configurez une base de données PostgreSQL (optionnel)
3. Ajustez les paramètres de sécurité selon vos besoins

## Structure du projet
```
/
├── models/             # Modèles de données
├── routes/             # Routes et contrôleurs
├── services/           # Logique métier
├── templates/          # Templates HTML
├── static/             # CSS, JS, images
├── app.py             # Configuration Flask
├── main.py            # Point d'entrée
└── README.md          # Ce fichier
```

## Utilisation
1. Accédez au tableau de bord principal
2. Ajoutez vos premiers produits
3. Enregistrez les mouvements de stock
4. Consultez les statistiques et alertes

## Support
- Interface entièrement en français
- Documentation intégrée dans l'application
- Système d'aide contextuelle

## Licence
Libre d'utilisation pour usage commercial et personnel.