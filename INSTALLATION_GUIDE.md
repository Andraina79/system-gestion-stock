# Guide d'Installation - Système de Gestion de Stock

## 📦 Comment télécharger et installer votre application

### Étape 1: Télécharger tous les fichiers
Dans Replit, vous devez télécharger tous ces dossiers et fichiers :

```
📁 Votre projet/
├── 📁 models/
│   ├── product.py
│   └── stock_movement.py
├── 📁 routes/
│   ├── main_routes.py
│   ├── product_routes.py
│   ├── movement_routes.py
│   └── statistics_routes.py
├── 📁 services/
│   ├── inventory_service.py
│   └── statistics_service.py
├── 📁 templates/
│   ├── 📁 products/
│   ├── 📁 movements/
│   ├── 📁 statistics/
│   ├── 📁 alerts/
│   ├── base.html
│   └── index.html
├── 📁 static/
│   ├── 📁 css/
│   │   └── custom.css
│   └── 📁 js/
│       └── main.js
├── app.py
├── main.py
└── README.md
```

### Étape 2: Installation des dépendances
Créez un fichier `requirements.txt` avec ce contenu :
```
flask
flask-sqlalchemy
gunicorn
email-validator
psycopg2-binary
```

Puis installez avec :
```bash
pip install -r requirements.txt
```

### Étape 3: Configuration
1. **Variable d'environnement** :
```bash
export SESSION_SECRET="votre-cle-secrete-tres-longue-et-complexe"
```

2. **Pour Windows** :
```cmd
set SESSION_SECRET=votre-cle-secrete-tres-longue-et-complexe
```

### Étape 4: Lancement
```bash
python main.py
```

Votre application sera accessible sur : http://localhost:5000

## 🌐 Déploiement sur site web

### Option A: Hébergement gratuit

#### 1. **Heroku** (gratuit)
1. Créez un compte sur heroku.com
2. Installez Heroku CLI
3. Commandes :
```bash
heroku create votre-app-stock
git add .
git commit -m "Application de gestion de stock"
git push heroku main
```

#### 2. **Railway** (gratuit)
1. Connectez votre compte GitHub
2. Importez votre projet
3. Railway détecte automatiquement Flask
4. URL automatique fournie

#### 3. **Render** (gratuit)
1. Connectez GitHub à render.com
2. Sélectionnez votre repository
3. Type: Web Service
4. Commande de build : `pip install -r requirements.txt`
5. Commande de start : `gunicorn main:app`

### Option B: Serveur web personnel

#### Apache + mod_wsgi
1. Installez mod_wsgi
2. Configurez Virtual Host
3. Pointez vers votre application Flask

#### Nginx + Gunicorn
1. Installez nginx et gunicorn
2. Configurez nginx pour proxy vers gunicorn
3. Lancez avec : `gunicorn --bind 127.0.0.1:5000 main:app`

## 🔧 Configuration de production

### Sécurité
- Changez la clé secrète
- Utilisez HTTPS
- Configurez un pare-feu

### Performance
- Utilisez une base de données PostgreSQL
- Configurez la mise en cache
- Optimisez les images

### Sauvegarde
- Sauvegardez régulièrement les données
- Testez la restauration
- Documentez les procédures

## 📞 Support
Votre système est maintenant prêt pour un usage professionnel !