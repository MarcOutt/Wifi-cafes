# Wifi-cafes

L'API RESTful Wifi-Cafés est une interface de programmation d'application basée sur Flask, permettant aux développeurs d'interagir avec une base de données de cafés. Elle offre diverses fonctionnalités, notamment l'exploration des cafés, l'ajout de nouveaux cafés et la mise à jour des informations sur ces établissements. Le stockage des données est assuré par SQLite.


## Fonctionnalités

- **Café Aléatoire :** Obtenir des informations sur un café au hasard dans la base de données.
- **Tous les Cafés :** Obtenir une liste de tous les cafés dans la base de données.
- **Rechercher des Cafés :** Trouver des cafés dans une localité spécifique.
- **Ajouter un Café :** Proposer un nouveau café avec des détails tels que le nom, l'emplacement et les équipements.
- **Mettre à Jour le Prix du Café :** Mettre à jour le prix du café pour un café spécifique.
- **Supprimer un Café :** Supprimer un café de la base de données (nécessite une clé API pour l'autorisation).

## Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-nom-utilisateur/application-recherche-cafes.git
   cd application-recherche-cafes```

2. Installez les dépendances:
   ```pip install -r requirements.txt```
   
4. Lancer l'application
   ```python app.py```


L'application sera accessible à l'adresse http://localhost:5000/


## Utilisation
Visitez la page d'accueil à [http://localhost:5000/](http://localhost:5000/) pour explorer l'application.

Utilisez les différentes routes pour interagir avec la base de données des cafés :

- `/random` : Obtenez des informations sur un café au hasard.
- `/all` : Récupérez une liste de tous les cafés.
- `/search?loc=<localite>` : Trouvez des cafés dans une localité spécifique.
- `/add` (POST) : Proposez un nouveau café.
- `/update-price/<cafe_id>` (PATCH) : Mettez à jour le prix du café.
- `/delete/<cafe_id>` (DELETE) : Supprimez un café (nécessite une clé API pour l'autorisation).


## Clé API

Pour effectuer certaines actions telles que la suppression d'un café, vous devez fournir une clé API dans la requête. La clé API pour ces actions est définie à "TopSecretAPIKey" dans l'implémentation actuelle.
   ```curl -X DELETE http://localhost:5000/update-price/1?api_key=TopSecretAPIKey```
