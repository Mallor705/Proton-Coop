# MultiScope

[Voir en portugais](README.pt.md) | [Voir en anglais](../README.md) | [Voir en espagnol](README.es.md)

# MultiScope

![Bannière MultiScope](https://github.com/Mallor705/MultiScope/assets/80993074/399081e7-295e-4c55-b040-02d242407559)

Permet de jouer à des titres Windows en mode coopératif local sous Linux, en exécutant plusieurs instances du même jeu via Proton et Gamescope, avec des profils indépendants et la prise en charge des contrôleurs.

## Caractéristiques Principales

- **Coopération Locale Avancée:** Exécutez jusqu'à deux instances du même jeu simultanément pour une expérience coopérative locale fluide.
- **Profils de Jeu Isolés:** Maintenez des sauvegardes et des configurations indépendantes pour chaque jeu grâce à des profils personnalisables.
- **Flexibilité d'Exécution:** Prend en charge la sélection de tout exécutable `.exe` et de diverses versions de Proton, y compris GE-Proton.
- **Résolution Personnalisable:** Ajustez la résolution pour chaque instance de jeu individuellement.
- **Débogage Simplifié:** Génération automatique de journaux pour faciliter l'identification et la correction des problèmes.
- **Mappage des Contrôleurs:** Configurez des contrôleurs physiques spécifiques pour chaque joueur.
- **Compatibilité Étendue:** Prend en charge plusieurs jeux via le système de profils.

## État du Projet

- **Fonctionnalité Principale:** Les jeux s'ouvrent dans des instances séparées avec des sauvegardes indépendantes.
- **Performances:** Performances optimisées pour une expérience de jeu fluide.
- **Gestion de Proton:** Version de Proton entièrement sélectionnable, y compris la prise en charge de GE-Proton.
- **Organisation:** Profils dédiés à chaque jeu.

### Problèmes Connus

- **Reconnaissance des Contrôleurs:** Dans certains cas, les contrôleurs peuvent ne pas être reconnus (priorité à la correction).
- **Disposition des Fenêtres:** Les instances peuvent s'ouvrir sur le même moniteur, nécessitant un déplacement manuel.

## Prérequis du Système

Pour assurer le bon fonctionnement de MultiScope, les prérequis suivants sont essentiels :

- **Steam:** Doit être installé et configuré sur votre système.
- **Proton:** Installez Proton (ou GE-Proton) via Steam.
- **Gamescope:** Installez Gamescope en suivant les [instructions officielles](https://github.com/ValveSoftware/gamescope).
- **Bubblewrap (`bwrap`):** Outil essentiel pour l'isolation des processus.
- **Permissions des Périphériques:** Assurez-vous d'avoir les permissions d'accès aux périphériques de contrôle dans `/dev/input/by-id/`.
- **Utilitaires Linux:** Bash et les utilitaires système Linux de base.
- **Python 3.8+:** Le projet nécessite Python version 3.8 ou supérieure.

## Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/Mallor705/MultiScope.git
    cd MultiScope
    ```
2.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

    Alternativement, si vous développez ou préférez une installation éditable :

    ```bash
    pip install -e .
    ```

## Comment Utiliser

### 1. Créer un Profil de Jeu

Créez un fichier JSON dans le dossier `profiles/` avec un nom descriptif (ex : `MonJeu.json`).

**Exemple de Contenu pour Écran Partagé Horizontal :**

```json
{
  "game_name": "JEU",
  "exe_path": ".steam/Steam/steamapps/common/JEU/game.exe",
  "players": [
    {
      "account_name": "Joueur1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Joueur2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "proton_version": "GE-Proton10-4",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": [
    "",
    ""
  ],
  "player_mouse_event_paths": [
    "",
    ""
  ],
  "player_keyboard_event_paths": [
    "",
    ""
  ],
  "app_id": "12345678",
  "game_args": "",
  "use_goldberg_emu": false,
  "env_vars": {
    "WINEDLLOVERRIDES": "",
    "MANGOHUD": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "horizontal",
    "instances": 2
  }
}
```

**Exemple de Contenu pour Écran Partagé Vertical :**

```json
{
  "game_name": "JEU",
  "exe_path": ".steam/Steam/steamapps/common/JEU/game.exe",
  "players": [
    {
      "account_name": "Joueur1",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000001"
    },
    {
      "account_name": "Joueur2",
      "language": "brazilian",
      "listen_port": "",
      "user_steam_id": "76561190000000002"
    }
  ],
  "proton_version": "GE-Proton10-4",
  "instance_width": 1920,
  "instance_height": 1080,
  "player_physical_device_ids": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],
  "player_mouse_event_paths": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],
  "player_keyboard_event_paths": [
    "/dev/input/by-id/...",
    "/dev/input/by-id/..."
  ],

  "player_audio_device_ids": [
    "",
    ""
  ],


  "app_id": "12345678",
  "game_args": "",
  "use_goldberg_emu": false,
  "env_vars": {
    "WINEDLLOVERRIDES": "",
    "MANGOHUD": "1"
  },
  "is_native": false,
  "mode": "splitscreen",
  "splitscreen": {
    "orientation": "vertical",
    "instances": 2
  }
}
```

### 2. Exécutez le Script Principal

À partir de la racine du projet, exécutez la commande, en remplaçant `<nom_du_profil>` par le nom de votre fichier JSON de profil (sans l'extension `.json`) :

```bash
python ./multiscope.py <nom_du_profil>
# Ou, si installé via setuptools :
multi-scope <nom_du_profil>
```

Après l'exécution, le script :

- Validera toutes les dépendances nécessaires.
- Chargera le profil de jeu spécifié.
- Créera des préfixes Proton séparés pour chaque instance de jeu.
- Lancera les deux fenêtres de jeu via Gamescope.
- Générera des journaux détaillés dans `~/.local/share/multi-scope/logs/` pour le débogage.

### 3. Mappage des Contrôleurs

- Les contrôleurs sont configurés dans le fichier de profil ou dans des fichiers spécifiques à l'intérieur de `controller_config/`.
- Pour éviter les conflits, les listes noires de contrôleurs (ex : `Player1_Controller_Blacklist`) sont générées automatiquement.
- **Important :** Connectez tous vos contrôleurs physiques avant de démarrer le script.

## Test de l'Installation

Pour vérifier que les prérequis sont correctement installés, exécutez les commandes suivantes :

```bash
gamescope --version
bwrap --version
```

## Conseils et Dépannage

-   **Contrôleurs non reconnus :** Vérifiez les permissions dans `/dev/input/by-id/` et confirmez que les ID des périphériques sont corrects dans votre fichier de profil.
-   **Proton introuvable :** Assurez-vous que le nom de la version de Proton dans votre profil correspond exactement au nom d'installation dans Steam.
-   **Instances sur le même moniteur :** Les instances de jeu peuvent s'ouvrir sur le même moniteur. Pour les déplacer et les organiser, vous pouvez utiliser les raccourcis clavier suivants. **Notez que les raccourcis peuvent varier en fonction de votre environnement de bureau Linux et de vos paramètres personnalisés :**
      *   `Super + W` (ou `Ctrl + F9` / `Ctrl + F10`) : Affiche un aperçu de tous les espaces de travail et des fenêtres ouvertes (Activités/Aperçu), similaire au survol de la souris dans le coin supérieur gauche.
      *   `Super + Flèches (↑ ↓ ← →)` : Déplace et ancre la fenêtre active sur un côté de l'écran.
      *   `Super + PgDn` : Minimise la fenêtre active.
      *   `Super + PgUp` : Maximise la fenêtre active.
      *   `Alt + Tab` : Bascule entre les fenêtres ouvertes de différentes applications.
      *   `Super + D` : Minimise toutes les fenêtres et affiche le bureau.
-   **Journaux de débogage :** Consultez le répertoire `~/.local/share/multi-scope/logs/` pour obtenir des informations détaillées sur les erreurs et le comportement du script.

## Remarques Importantes

-   Testé et optimisé avec Palworld, mais peut être compatible avec d'autres jeux (peut nécessiter des ajustements dans le fichier de profil).
-   Actuellement, le script ne prend en charge qu'une configuration à deux joueurs.
-   Pour les jeux qui ne prennent pas en charge nativement plusieurs instances, des solutions supplémentaires telles que des sandboxes ou des comptes Steam séparés pourraient être nécessaires.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou des pull requests.

## Licence

Ce projet est distribué sous la licence MIT. Consultez le fichier `LICENSE` dans le dépôt pour plus de détails.
