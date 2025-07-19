# 🕷️ SPIDER INTEL — Plateforme de veille OSINT

**SPIDER INTEL** est une application de cybersécurité conçue pour réaliser une veille intelligente sur les adresses IP à l’aide de sources OSINT. Elle intègre :

- 🔎 Analyse IP en temps réel (Shodan, AbuseIPDB, IP-API)
- 🤖 Bot Telegram connecté via Webhook (commandes `/start` et `/scan <ip>`)
- 🌐 Interface web FastAPI avec formulaire de scan IP
- 📄 Génération PDF (bientôt)
- 🚀 Déploiement complet sur Render
- 🛡️ Projet à but éducatif dans un cadre légal

## ⚙️ Technologies utilisées

- **Python 3.11.9**
- **FastAPI** + **Jinja2**
- **Telegram Bot API**
- **Shodan / AbuseIPDB / IP-API**
- **WeasyPrint** (PDF)
- **Render.com** pour l’hébergement

## 🧪 Fonctionnalités clés

### ✅ Scan IP via Bot Telegram

- `/start` → message de bienvenue
- `/scan 8.8.8.8` → scan OSINT de l’adresse IP

> Réponse du bot : pays, score d’abus, organisation, résumé...

---

### ✅ Interface Web

- Interface sécurisée avec FastAPI + Jinja2
- Saisie manuelle d’une IP à scanner
- Résultats affichés directement dans le navigateur

---

## 📁 Structure du projet (simplifiée)

spider_intel/
├── app/
│ ├── main.py # Point d’entrée FastAPI
│ ├── templates/ # Interface HTML (index.html)
│ ├── routes/ # email_route.py, auth_route.py
│ ├── scanner/ # email_scanner.py
│ └── telegram/ # webhook.py, set_webhook.py
├── .env # Clés API (non inclus)
├── requirements.txt
├── render.yaml
└── README.md


## 🚀 Déploiement Render

- Python version forcée via `runtime.txt` (`python-3.11.9`)
- Fichier `render.yaml` configuré pour lancer FastAPI
- Webhook Telegram fonctionnel même si l’app est fermée localement

  
## 🔐 Sécurité

- Clés API stockées dans `.env` (jamais commité)
- Fichier `.gitignore` protège `.env`, `.venv`, et autres sensibles
- Utilisation future de Supabase pour stockage sécurisé
## 🧠 Auteurs

- **Thomas Ouattara** – Développeur et porteur du projet
## ⚠️ Avertissement
> Ce projet est un outil pédagogique de cybersécurité à utiliser exclusivement dans un cadre légal.  
> SPIDER INTEL **ne doit pas être utilisé pour scanner des adresses sans autorisation**.

-------------------------------------------------------------------------------------------------------





