# BookHub

Une plateforme de vente de livres en ligne développée avec Django.

## Fonctionnalités

- **Gestion des utilisateurs** : Inscription, connexion, profils clients et administrateurs
- **Catalogue de livres** : Navigation par catégories, recherche, détails des livres
- **Panier d'achat** : Ajout/suppression d'articles, gestion des quantités
- **Commandes** : Processus de commande complet avec suivi du statut
- **Panel administrateur** : Gestion des livres, utilisateurs et commandes

## Technologies utilisées

- **Backend** : Django 4.2.7
- **Base de données** : SQLite
- **Frontend** : HTML, CSS, JavaScript
- **Images** : Pillow pour la gestion des images

## Installation

1. Clonez le projet :
```bash
git clone <url-du-repo>
cd bookHub
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Effectuez les migrations :
```bash
python manage.py migrate
```

5. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancez le serveur :
```bash
python manage.py runserver
```

## Structure du projet

```
bookHub/
├── BookHub/          # Configuration Django
├── core/             # Application principale
│   ├── models.py     # Modèles (User, Book, Order, etc.)
│   ├── views.py      # Vues
│   ├── templates/    # Templates HTML
│   └── static/       # Fichiers CSS
├── media/            # Images uploadées
└── manage.py         # Script de gestion Django
```

## Modèles principaux

- **User** : Utilisateurs avec rôles (client/admin)
- **Book** : Livres avec auteur, catégorie, prix, stock
- **Category** : Catégories de livres
- **Author** : Auteurs des livres
- **Cart/CartItem** : Panier d'achat
- **Order/OrderItem** : Commandes et articles commandés

## Utilisation

1. Accédez à `http://127.0.0.1:8000/`
2. Créez un compte ou connectez-vous
3. Parcourez le catalogue de livres
4. Ajoutez des livres au panier
5. Passez commande

## Administration

Accédez au panel admin à `/admin/` avec vos identifiants superutilisateur pour :
- Gérer les livres et catégories
- Voir les commandes
- Administrer les utilisateurs