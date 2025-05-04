import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==== CONFIG DNA CENTER ====
DNAC_URL = "https://dnac.example.com"          # Altere para o endereço do seu DNAC
DNAC_USER = "seu_usuario"                      # Altere para seu usuário
DNAC_PASSWORD = "sua_senha"                    # Altere para sua senha

# ==== CONFIG GRAFANA ====
GRAFANA_URL = "http://localhost:3000"          # Altere se necessário
GRAFANA_API_KEY = "Bearer SUA_CHAVE_GRAFANA"  # Não esqueça do prefixo "Bearer"
DASHBOARD_UID = "UID_DA_DASHBOARD"            # O UID da dashboard onde está a variável

def get_dnac_token():
    url = f"{DNAC_URL}/dna/system/api/v1/auth/token"
    try:
        response = requests.post(url, auth=(DNAC_USER, DNAC_PASSWORD), verify=False)
        response.raise_for_status()
        token = response.json()["Token"]
        print("[+] Token do DNA obtido com sucesso.")
        return token
    except Exception as e:
        print(f"[-] Erro ao obter token do DNA: {e}")
        return None

def update_grafana_variable(new_value):
    headers = {
        "Authorization": GRAFANA_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        # Buscar dashboard
        response = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}", headers=headers)
        response.raise_for_status()
        dashboard_data = response.json()
        dashboard = dashboard_data["dashboard"]

        # Atualizar variável 'teste'
        for variable in dashboard.get("templating", {}).get("list", []):
            if variable["name"] == "teste":
                variable["type"] = "custom"
                variable["query"] = new_value
                variable["options"] = [
                    {"text": new_value, "value": new_value, "selected": True}
                ]
                variable["current"] = {
                    "text": new_value,
                    "value": new_value,
                    "selected": True
                }
                variable["hide"] = 2  # Oculta a variável no painel

        dashboard["version"] += 1  # Incrementa a versão

        payload = {
            "dashboard": dashboard,
            "folderId": dashboard_data["meta"]["folderId"],
            "overwrite": True
        }

        response = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"[+] Variável 'teste' atualizada com valor (oculto): {new_value}")
    except Exception as e:
        print(f"[-] Erro ao atualizar Grafana: {e}")

# === LOOP PRINCIPAL ===
while True:
    print("[*] Iniciando ciclo de atualização...")
    token = get_dnac_token()
    if token:
        update_grafana_variable(token)  # Usa o token completo
    else:
        print("[-] Token não obtido, pulando atualização.")

    print("[*] Aguardando 45 minutos (2700 segundos)...\n")
    time.sleep(2700)
