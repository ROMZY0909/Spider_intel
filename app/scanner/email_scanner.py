import os
import requests
import shodan
from dotenv import load_dotenv

load_dotenv()

# 🔐 Chargement des clés API
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
IPAPI_KEY = os.getenv("IPAPI_KEY")  # Exemple : http://ip-api.com/json/

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
        url = f"{IPAPI_KEY}{ip}"  # Ex: http://ip-api.com/json/8.8.8.8
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

# === Fonction principale combinée avec résumé ===
def full_osint_lookup(ip):
    ipapi_data = lookup_ipapi(ip)
    shodan_data = lookup_shodan(ip)
    abuse_data = lookup_abuseipdb(ip)

    summary = []

    # Résumé IP-API
    if "error" not in ipapi_data:
        summary.append(f"🌍 Localisation : {ipapi_data.get('country', 'Inconnue')}, {ipapi_data.get('regionName', '')}, {ipapi_data.get('city', '')}")
        summary.append(f"🌐 FAI : {ipapi_data.get('isp', 'N/A')}")
    else:
        summary.append(f"❌ IP-API : {ipapi_data['error']}")

    # Résumé Shodan
    if "error" not in shodan_data:
        summary.append(f"🏢 Organisation : {shodan_data.get('org', 'N/A')}")
        summary.append(f"🖥️ OS : {shodan_data.get('os', 'Inconnu')}")
        summary.append(f"🔌 Ports ouverts : {', '.join(map(str, shodan_data.get('ports', [])))}")
    else:
        summary.append(f"❌ Shodan : {shodan_data['error']}")

    # Résumé AbuseIPDB
    if "error" not in abuse_data:
        abuse_score = abuse_data.get("data", {}).get("abuseConfidenceScore", "N/A")
        summary.append(f"⚠️ Score de confiance AbuseIPDB : {abuse_score}/100")
    else:
        summary.append(f"❌ AbuseIPDB : {abuse_data['error']}")

    return {
        "ipapi": ipapi_data,
        "shodan": shodan_data,
        "abuseipdb": abuse_data,
        "summary": "\n".join(summary)
    }

# === Alias pour compatibilité avec anciens scripts ===
def scan_email(ip: str):
    return full_osint_lookup(ip)
