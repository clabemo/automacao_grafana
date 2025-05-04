import requests
import time
import urllib3
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Desativa warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===== ESTRUTURAS DE CONFIGURAÇÃO =====
@dataclass
class APIConfig:
    enabled: bool
    url: str
    auth: Dict[str, str]
    var_name: str = "teste"
    dashboard_uid: str = ""

# Configurações
DNAC = APIConfig(
    enabled=True,
    url="https://dnac.example.com",
    auth={"user": "seu_usuario", "password": "sua_senha"},
)

GRAFANA = APIConfig(
    enabled=True,
    url="http://localhost:3000",
    auth={"api_key": "Bearer SUA_CHAVE_GRAFANA"},
    dashboard_uid="UID_DA_DASHBOARD",
    var_name="teste"
)

# ===== FUNÇÕES PRINCIPAIS =====
def get_dnac_token() -> Optional[str]:
    """Obtém token do DNA Center ou retorna valor simulado se desativado"""
    if not DNAC.enabled:
        print("[MOCK] DNA Center desativado - Retornando token simulado")
        return "MOCK_TOKEN_" + str(int(time.time()))
    
    try:
        response = requests.post(
            f"{DNAC.url}/dna/system/api/v1/auth/token",
            auth=(DNAC.auth["user"], DNAC.auth["password"]),
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["Token"]
    except Exception as e:
        print(f"[DNA Center] Erro: {str(e)[:100]}...")  # Limita tamanho do erro
        return None

def update_grafana_variable(value: str) -> bool:
    """Atualiza variável no Grafana ou simula se desativado"""
    if not GRAFANA.enabled:
        print(f"[MOCK] Grafana desativado - Simulando update para valor: {value}")
        return True
    
    headers = {
        "Authorization": GRAFANA.auth["api_key"],
        "Content-Type": "application/json"
    }
    
    try:
        # 1. Buscar dashboard
        print(f"[Grafana] Buscando dashboard {GRAFANA.dashboard_uid}...")
        dashboard_url = f"{GRAFANA.url}/api/dashboards/uid/{GRAFANA.dashboard_uid}"
        response = requests.get(dashboard_url, headers=headers, timeout=10)
        response.raise_for_status()
        dashboard_data = response.json()
        
        # 2. Localizar e atualizar variável
        variables = dashboard_data["dashboard"].get("templating", {}).get("list", [])
        target_var = next((v for v in variables if v["name"] == GRAFANA.var_name), None)
        
        if not target_var:
            print(f"[Grafana] Variável '{GRAFANA.var_name}' não encontrada!")
            return False
            
        target_var.update({
            "type": "custom",
            "query": value,
            "options": [{"text": value, "value": value, "selected": True}],
            "current": {"text": value, "value": value, "selected": True},
            "hide": 2
        })
        
        # 3. Enviar atualização
        print(f"[Grafana] Enviando atualização para variável '{GRAFANA.var_name}'...")
        update_response = requests.post(
            f"{GRAFANA.url}/api/dashboards/db",
            headers=headers,
            json={
                "dashboard": dashboard_data["dashboard"],
                "folderId": dashboard_data["meta"]["folderId"],
                "overwrite": True
            },
            timeout=15
        )
        update_response.raise_for_status()
        print("[Grafana] Dashboard atualizado com sucesso!")
        return True
        
    except requests.Timeout:
        print("[Grafana] Timeout - Servidor não respondeu a tempo")
        return False
    except Exception as e:
        print(f"[Grafana] Erro: {str(e)[:200]}...")  # Limita tamanho do erro
        return False

# ===== TESTES E CONTROLE =====
def run_test_mode():
    """Modo de teste manual com interação do usuário"""
    print("\n" + "="*40)
    print("MODO DE TESTE DO GRAFANA".center(40))
    print("="*40)
    
    while True:
        test_value = input("\nDigite um valor para teste (ou 'sair'): ").strip()
        if test_value.lower() == 'sair':
            break
            
        if test_value:
            success = update_grafana_variable(test_value)
            print("✅ Sucesso!" if success else "❌ Falha!")
        else:
            print("Por favor, digite um valor válido")

def main_loop(interval: int = 2700):
    """Loop principal de execução automática"""
    print("\nIniciando operação automática...")
    print(f"Configuração atual:\n- DNA Center: {'ON' if DNAC.enabled else 'OFF'}\n- Grafana: {'ON' if GRAFANA.enabled else 'OFF'}")
    
    while True:
        print("\n" + "="*30)
        print(f"Ciclo iniciado em {time.strftime('%H:%M:%S')}")
        
        token = get_dnac_token()
        if token or not DNAC.enabled:
            update_grafana_variable(token if DNAC.enabled else "SIMULATED_VALUE")
        else:
            print("⚠️ Não foi possível obter token do DNA Center")
        
        print(f"Aguardando próximo ciclo ({interval//60} minutos)...")
        time.sleep(interval)

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    print("""\n=== Sistema de Atualização Grafana/DNA Center ===
    
Modos de operação disponíveis:
1. Modo Automático (ambas APIs)
2. Testar apenas Grafana (interativo)
3. Modo Automático sem DNA Center
4. Modo Automático sem Grafana
5. Sair
""")
    
    choice = input("Escolha o modo de operação: ").strip()
    
    if choice == "1":
        DNAC.enabled = True
        GRAFANA.enabled = True
        main_loop()
    elif choice == "2":
        run_test_mode()
    elif choice == "3":
        DNAC.enabled = False
        GRAFANA.enabled = True
        main_loop()
    elif choice == "4":
        DNAC.enabled = True
        GRAFANA.enabled = False
        main_loop()
    else:
        print("Operação encerrada")