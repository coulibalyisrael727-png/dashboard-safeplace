# Déploiement sur Railway

## Pré-requis
- Avoir un compte Railway
- Un repo GitHub public ou privé contenant `dashboard-service`

## Étapes

1. Créer un dépôt GitHub pour `dashboard-service`
2. Dans le dossier `dashboard-service`: 
   ```powershell
   cd 'C:\Users\couli\Desktop\Nouveau dossier (3)\dashboard-service'
   git remote add origin https://github.com/<ton-utilisateur>/<repo-dashboard>.git
   git push -u origin master
   ```
3. Sur Railway :
   - Créer un nouveau projet
   - Choisir « Deploy from GitHub »
   - Sélectionner le repo `dashboard-service`
   - Railway détectera le `Dockerfile` ou le `Procfile`

## Variables d'environnement
Ajouter ces variables dans Railway :

- `DJANGO_SECRET_KEY` : une clé secrète forte
- `DJANGO_DEBUG` : `False`
- `ALLOWED_HOSTS` : `*` ou le domaine Railway
- `MAIN_API_URL` : l’URL publique de l’API principale, par exemple `https://mon-app-principale.railway.app/api/v1/`
- `MAIN_SITE_URL` : l’URL publique de l’application principale, par exemple `https://mon-app-principale.railway.app`

## Notes importantes
- Le projet utilise actuellement SQLite (`db.sqlite3`). Pour un déploiement stable, il est préférable de migrer vers PostgreSQL ou une base de données managée.
- Le `Dockerfile` est configuré pour exécuter `gunicorn` en production.
- `WhiteNoise` est ajouté pour servir les fichiers statiques en production.

## Commandes utiles

Pour tester localement :
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 8001
```

---

# Déploiement sur Vercel

## Pré-requis
- Avoir un compte Vercel
- Un repo GitHub connecté à Vercel

## Étapes

1. Connecter ton repo GitHub à Vercel
2. Vercel détectera automatiquement la configuration via `vercel.json` et `api/index.py`
3. Le déploiement se lance automatiquement

## Variables d'environnement sur Vercel
Dans les settings du projet Vercel :

- `DJANGO_SETTINGS_MODULE` : `dashboard_project.settings`
- `DJANGO_DEBUG` : `False`
- `ALLOWED_HOSTS` : `dashboard-safeplace-4o77xo41w-coulibalyisrael727-pngs-projects.vercel.app,localhost,127.0.0.1`
- `SECRET_KEY` : une clé secrète forte (ou utiliser `@django-secret-key` pour une variable secrète)
- `MAIN_API_URL` : l'URL publique de l'API principale
- `MAIN_SITE_URL` : l'URL publique de l'application principale

## Notes importantes pour Vercel
- Vercel utilise des fonctions serverless, donc SQLite peut poser des problèmes de persistance
- Pour la production, envisager une base de données externe (PostgreSQL)
- Les fichiers statiques sont servis via `WhiteNoise`
- Le fichier `api/index.py` est le point d'entrée pour Vercel
