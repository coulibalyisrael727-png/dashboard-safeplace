# Déploiement sur Netlify

## Pré-requis
- Avoir un compte Netlify
- Un repo GitHub connecté à Netlify

## Étapes

1. Connecter ton repo GitHub à Netlify
2. Netlify détectera automatiquement la configuration via `netlify.toml`
3. Le déploiement se lance automatiquement

## Configuration Netlify
Le fichier `netlify.toml` configure :
- Build command : installation des dépendances et collecte des fichiers statiques
- Publish directory : `staticfiles/`
- Environment variables
- Redirects vers la fonction serverless

## Variables d'environnement
Définies dans `netlify.toml` :
- `DJANGO_SETTINGS_MODULE` : `dashboard_project.settings`
- `DJANGO_DEBUG` : `False`
- `ALLOWED_HOSTS` : domaine Netlify + localhost
- `SECRET_KEY` : clé de production
- `MOCK_API_DATA` : `True` (données fictives)

## Fonction Serverless
- `netlify/functions/django.py` : fonction qui sert l'application Django
- Toutes les routes sont redirigées vers cette fonction

## Fichiers statiques
- Servis depuis `staticfiles/`
- Collectés automatiquement lors du build

## Test du déploiement
Après déploiement, teste :
- `https://ton-domaine.netlify.app/test/` (endpoint de test)
- `https://ton-domaine.netlify.app/` (dashboard principal)

## Notes importantes
- Netlify utilise des fonctions serverless pour Django
- Les données sont mockées (MOCK_API_DATA=True)
- Pour connecter à l'API réelle, change MOCK_API_DATA=False et configure MAIN_API_URL

---

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
- `MAIN_API_URL` : l'URL publique de l'API principale, par exemple `https://mon-app-principale.railway.app/api/v1/`
- `MAIN_SITE_URL` : l'URL publique de l'application principale, par exemple `https://mon-app-principale.railway.app`

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
