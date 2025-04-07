

```markdown
# 🌙 NOCTÆ Discord Bot

Bot Discord esthétique et personnalisé pour l’accueil, la gestion des rôles linguistiques et l’affichage des règles via boutons.  
A soft and aesthetic Discord bot for welcome, language roles, and rules with button interactions.

🧚 **Usage privé uniquement — non destiné à une publication publique ou globale.**  
🧚 **Private-use only — not intended for public or global deployment.**

---

## 🛠️ Installation

### 🇫🇷 Étapes d’installation
1. Clonez ce repo :
```bash
git clone https://github.com/blgperfect/noctae.git
cd noctae
```

2. (Optionnel) Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate pour Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

---

### 🇬🇧 Installation Steps
1. Clone this repository:
```bash
git clone https://github.com/blgperfect/noctae.git
cd noctae
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration : `.env`

### 🇫🇷 Exemple de `.env` :
```env
DISCORD_TOKEN=        # Ton token Discord
MONGO_URI=            # (optionnel) URI MongoDB si tu l’utilises
DATABASE_NAME=        # (optionnel) Nom de ta base de données
```

### 🇬🇧 `.env` example:
```env
DISCORD_TOKEN=        # Your Discord bot token
MONGO_URI=            # (optional) MongoDB URI if you're using it
DATABASE_NAME=        # (optional) Your database name
```

⚠️ **Ne partage jamais ce fichier / Never share this file!** Il contient des infos sensibles.

---

## ⚙️ Personnalisation / Customization

### 🇫🇷 Tu peux facilement modifier :
- Les **ID de rôles, salons, catégories** dans les fichiers Python.
- Les **textes, couleurs, images, embeds, règles**.
- Les **permissions** des commandes (`admin_only`, etc).

### 🇬🇧 You can easily customize:
- **Role IDs, channel IDs, category IDs** inside Python files.
- All **texts, colors, images, embeds, and rules**.
- **Permissions** for commands (e.g., admin-only).

📌 **Pense à remplacer tous les ID d'exemple (13586...) par les tiens.**  
📌 **Make sure to replace all placeholder IDs (13586...) with your actual ones.**

---

## 🚀 Lancement / Run

### 🇫🇷 Pour lancer le bot :
```bash
python main.py
```

### 🇬🇧 To run the bot:
```bash
python main.py
```
```

