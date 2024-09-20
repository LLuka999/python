"""
Requêtes HTTP en Python avec requests
- GET
- POST
- Gestion des erreurs
"""
import requests

# Requête GET
try:
    response = requests.get("https://httpbin.org/get", timeout=5)
    print("GET /get :", response.status_code)
    print(response.json())
except Exception as e:
    print("Erreur GET :", e)

# Requête POST
try:
    response = requests.post("https://httpbin.org/post", data={"nom": "Alice"}, timeout=5)
    print("\nPOST /post :", response.status_code)
    print(response.json())
except Exception as e:
    print("Erreur POST :", e) 