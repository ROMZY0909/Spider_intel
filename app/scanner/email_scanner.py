import os
import requests
import shodan
from dotenv import load_dotenv

load_dotenv()

# Chargement des clés API depuis .env
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
IPAPI_KEY = os.getenv("IPAPI_KEY")  # C’est l’URL de base, ex: http://ip-api.com/json/

# === SHODAN LOOKUP ===
def lookup_shodan(ip):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.host(ip)
        return {
            "ip": result.get("ip_str"),
            "hostname": result.get("hostnames"),
            "org": result.get("org"),
            "os": result.get("os"),
            "ports": result.get("ports")
        }
    except Exception as e:
        return {"error": f"Shodan error: {str(e)}"}

# === IP-API LOOKUP ===
def lookup_ipapi(ip):
    try:
        url = f"{IPAPI_KEY}{ip}"  # IPAPI_KEY contient déjà http://ip-api.com/json/
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return {"error": f"IP-API error: {str(e)}"}

# === ABUSEIPDB LOOKUP ===
def lookup_abuseipdb(ip):
    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Key": ABUSEIPDB_API_KEY,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": "90"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"error": f"AbuseIPDB error: {str(e)}"}

# === Fonction principale combinée ===
def full_osint_lookup(ip):
    return {
        "ipapi": lookup_ipapi(ip),
        "shodan": lookup_shodan(ip),
        "abuseipdb": lookup_abuseipdb(ip)
    }

# === Alias pour compatibilité avec les autres scripts ===
def scan_email(ip: str):
    return full_osint_lookup(ip)
