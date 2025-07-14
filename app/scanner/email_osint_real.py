import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search_hibp(email: str) -> list:
    key = os.getenv("HIBP_API_KEY")
    if not key:
        return ["❌ API HIBP non configurée."]
    
    headers = {"hibp-api-key": key, "User-Agent": "SpiderIntel"}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=true"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = [b["Name"] for b in response.json()]
            return [f"✅ Leak détecté : {name}" for name in breaches]
        elif response.status_code == 404:
            return ["✅ Aucun leak détecté."]
        else:
            return [f"⚠️ Erreur API HIBP : {response.status_code}"]
    except Exception as e:
        return [f"Erreur HIBP : {str(e)}"]

def search_censys(email: str) -> list:
    # Simulé pour le moment
    return [f"📡 Résultat Censys simulé pour {email}"]

def search_shodan(email: str) -> list:
    # Simulé pour le moment
    return [f"🔎 Recherche Shodan simulée pour {email}"]
