# Dashboard Microservice — The SafePlace

## 📋 Vue d'ensemble

Ce microservice est une application Django indépendante qui sert de tableau de bord administratif pour The SafePlace. Il communique avec l'application principale via des API REST.

## 🏗️ Architecture Découplée

Ce microservice est une application Django indépendante hébergée sur **Netlify**. Elle communique avec le backend `podcastSafe` via des API REST.

### Flux de données
- **Frontend** : Django templates rendus par le microservice.
- **Backend API** : L'application principale fournit les données.
- **Proxy Netlify** : Le fichier `netlify.toml` redirige les appels `/api/*` vers le backend pour éviter les erreurs CORS.

## 🚀 Installation Locale

### Prérequis
- Python 3.11+
- Un backend `podcastSafe` en cours d'exécution (port 8000).

### Lancement
```bash
cd dashboard-service
python -m venv venv
# Activer l'environnement (Windows: venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env
# Configurer MAIN_API_URL=http://localhost:8000/api/v1/
python manage.py migrate
python manage.py runserver 8001
```

## 🌐 Déploiement (Netlify)

1. **GitHub** : Poussez ce dossier (`dashboard-service`) dans son propre dépôt.
2. **Netlify** : Créez un nouveau site à partir de ce dépôt.
3. **Configuration** : Netlify utilisera automatiquement `netlify.toml`.
4. **Variables d'environnement** :
   - `MAIN_API_URL` : L'URL de votre backend Django en production.
   - `DASHBOARD_API_KEY` : La clé secrète identique à celle du backend.

### Ports par défaut
- Dashboard : http://localhost:8001
- API principale : http://localhost:8000/api/v1/

## 📊 Fonctionnalités

### Dashboard principal
- Statistiques en temps réel
- Épisodes récents
- Analytics détaillées
- Gestion des donations

### Points d'accès API
- `/` : Dashboard principal
- `/analytics/` : Analytics détaillées
- `/episodes/` : Gestion des épisodes
- `/donations/` : Gestion des donations
- `/health/` : Health check

## 🔐 Sécurité

### Authentification
- Login requis pour accéder au dashboard
- API Key authentication pour la communication avec le site principal
- CORS configuré pour les origines autorisées
- La clé API `DASHBOARD_API_KEY` doit correspondre entre les deux services

### Permissions
- Seuls les utilisateurs authentifiés peuvent accéder aux données
- Validation des entrées API
- Protection contre les injections

## 🌐 API Endpoints

### Données du dashboard
```
GET /api/v1/dashboard-data/
Authorization: Bearer <token>
```

### Analytics
```
GET /api/v1/analytics/?days=30
Authorization: Bearer <token>
```

### Épisodes
```
GET /api/v1/episodes/?page=1&status=published&search=terme
Authorization: Bearer <token>
```

### Donations
```
GET /api/v1/donations/?page=1&status=completed
Authorization: Bearer <token>
```

## 🔄 Déploiement

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  dashboard:
    build: ./dashboard-service
    ports:
      - "8001:8001"
    environment:
      - MAIN_APP_API_URL=https://main-app:8000/api/v1/
    depends_on:
      - main-app
```

## 📝 Développement

### Structure du projet
```
dashboard-service/
├── dashboard/              # Application Django
│   ├── views.py          # Vues du dashboard
│   ├── templates/        # Templates HTML
│   └── models.py        # Modèles (si nécessaire)
├── dashboard_project/     # Configuration du projet
│   ├── settings.py       # Paramètres Django
│   ├── urls.py          # Routes URL
│   └── wsgi.py         # WSGI application
├── static/              # Fichiers statiques
├── media/               # Fichiers médias
├── requirements.txt      # Dépendances Python
└── manage.py           # Script de gestion Django
```

### Ajouter de nouvelles fonctionnalités
1. Créer les vues dans `dashboard/views.py`
2. Ajouter les routes dans `dashboard_project/urls.py`
3. Créer les templates dans `dashboard/templates/`
4. Ajouter les endpoints API dans l'application principale

## 🐛 Debugging

### Problèmes courants
- **Connexion API refusée** : Vérifier CORS et URLs
- **Données vides** : Vérifier l'authentification
- **Erreur 404** : Vérifier les routes URL

### Logs
```bash
# Logs Django
python manage.py runserver --verbosity=2

# Logs détaillés
tail -f logs/django.log
```

## 📈 Monitoring

### Health check
```bash
curl http://localhost:8001/health/
```

### Métriques
- Temps de réponse API
- Taux de succès/échec
- Utilisation mémoire/CPU

## 🔗 Intégration

### Avec l'application principale
1. L'application principale expose les endpoints API
2. Le dashboard consomme ces endpoints
3. Authentification partagée via tokens

### Services externes
- Stripe (pour les donations)
- Analytics (Google Analytics, etc.)
- Stockage (AWS S3, etc.)

## 📞 Support

### Documentation
- API REST : Documentation des endpoints
- Frontend : Guide des composants
- Backend : Architecture et modèles

### Contact
- Issues GitHub : Signaler les bugs
- Documentation : Wiki du projet
