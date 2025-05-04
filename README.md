# 🔄 Atualizador de Variáveis Grafana + DNA Center

Este script automatiza a atualização de variáveis em dashboards do Grafana usando tokens de autenticação do Cisco DNA Center.


## 📋 Descrição

- O script obtém periodicamente (a cada 45 minutos) um token de acesso à API do Catalyst Center.
- Esse token é usado para atualizar uma variável em um dashboard do Grafana.
- A variável é atualizada de forma **oculta**, garantindo segurança no uso do token.

## 📋 Pré-requisitos

- Python 3.8+
- Acesso administrativo ao Grafana
- Credenciais do DNA Center (se aplicável)
- Bibliotecas: requests, urllib3

## ⚙️ Configuração
Edite as variáveis no arquivo config.py (ou no cabeçalho do script):

### DNA Center
DNAC_URL = "https://dnac.example.com"
DNAC_USER = "seu_usuario"
DNAC_PASSWORD = "sua_senha"

### Grafana
GRAFANA_URL = "http://localhost:3000"
GRAFANA_API_KEY = "Bearer sua_chave_api"
DASHBOARD_UID = "uid_do_seu_dashboard"
VARIABLE_NAME = "nome_da_variavel"

## 🚀 Como usar

python atualizador_grafana.py

## 🎛 Modos de Operação

Modo Automático Completo
Atualiza Grafana com token real do DNA Center
Ciclo a cada 45 minutos
Modo Teste Grafana
Permite testar com valores customizados
Ideal para validação inicial
Modo Sem DNA Center
Usa valores simulados para teste contínuo
Modo Sem Grafana
Apenas monitora token do DNA Center

## 🔄 Fluxo de Operação
Obtém token de autenticação do DNA Center
Atualiza variável no dashboard do Grafana
Aguarda intervalo configurado (padrão: 45min)
Repete o processo

## 🛠 Troubleshooting
Erro de conexão com DNA Center
Verifique:
✅ URL correta
✅ Credenciais válidas
✅ Acesso à rede

Falha ao atualizar Grafana
Confira:
✅ UID do dashboard
✅ Nome exato da variável
✅ Permissões da API Key

## 📜 Logs de Exemplo
[12:00:00] Iniciando ciclo...
[DNA Center] Token obtido com sucesso
[Grafana] Variável 'status_api' atualizada
[12:00:02] Aguardando próximo ciclo (45 minutos)...

## ⚠️ Segurança
- Armazene credenciais em variáveis de ambiente
- Use HTTPS para todas as conexões
- Restrinja permissões da API Key do Grafana

## 📝 Licença
- MIT License - Livre para uso e modificação