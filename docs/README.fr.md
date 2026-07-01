# KindleBoard

**Version actuelle :** `V1.0`

KindleBoard est un tableau de bord auto-hébergé pour Kindle et écrans e-ink, conçu pour Docker. Il permet de transformer un ancien Kindle Paperwhite en panneau toujours visible pour un planning, une note ou une liste de tâches.

![Aperçu anglais de KindleBoard](preview.png)

KindleBoard est prévu pour un réseau privé de confiance. Si vous l’exposez à internet, utilisez un VPN, une authentification via proxy inverse ou une autre couche de contrôle d’accès.

## Fonctionnalités

- Planning hebdomadaire personnel avec horaires, jours de repos, notes et total automatique des heures.
- Prise en charge des horaires de nuit, par exemple `22:00` à `06:00`.
- Mode note avec grande typographie.
- Liste de tâches cliquable directement depuis Kindle.
- Interface d’administration pour modifier le contenu, changer de mode et choisir la langue.
- Page optimisée pour Kindle avec fort contraste et grand bouton d’actualisation.
- Une seule base SQLite pour le planning, les notes, les tâches, le mode d’affichage et la langue.
- Interface multilingue.
- Port par défaut : `10000`.

## Modes d’affichage

- **Schedule** : planning hebdomadaire et total des heures.
- **Memo** : grande note lisible.
- **To-do** : liste de tâches cliquable.

La page Kindle affiche uniquement le mode sélectionné.

## Installation Docker

Image recommandée :

```text
neil2046/kindleboard:latest
```

Image miroir :

```text
ghcr.io/neil2046/kindleboard:latest
```

```bash
mkdir kindleboard
cd kindleboard
```

Créer `docker-compose.yml` :

```yaml
services:
  kindleboard:
    image: neil2046/kindleboard:latest
    container_name: kindleboard
    ports:
      - "10000:10000"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Démarrer :

```bash
docker compose up -d
```

Accéder :

```text
Admin:  http://SERVER-IP:10000/admin
Kindle: http://SERVER-IP:10000/kindle
```

## Persistance des données

Les données sont stockées dans `./data/schedule.db`. Planning, notes, tâches, mode d’affichage et langue sont dans cette unique base SQLite.

Au premier démarrage, si `/data/schedule.db` n’existe pas, KindleBoard copie une base de démonstration en anglais. Les données existantes ne sont jamais écrasées.

## Mise à jour

```bash
docker compose pull
docker compose up -d
```

## Notes Kindle

- Ouvrez `http://SERVER-IP:10000/kindle` dans le navigateur Kindle.
- Le Kindle doit pouvoir accéder à l’hôte Docker.
- La page contient un grand bouton d’actualisation.
- Les barres du navigateur et l’écran de veille sont contrôlés par Kindle OS.

## Sécurité

KindleBoard ne propose pas de comptes utilisateurs ni de connexion. Utilisez-le dans un environnement de confiance. Pour un accès externe, utilisez un VPN ou un proxy inverse avec authentification.
