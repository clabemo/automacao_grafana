# 🔄 Integração Catalyst Center (DNA) + Grafana

Este projeto realiza a automação da atualização de uma variável em um dashboard do Grafana com o token gerado pela API do Cisco Catalyst Center (antigo DNA Center).

## 📋 Descrição

- O script obtém periodicamente (a cada 45 minutos) um token de acesso à API do Catalyst Center.
- Esse token é usado para atualizar uma variável chamada `teste` em um dashboard do Grafana.
- A variável é atualizada de forma **oculta**, garantindo segurança no uso do token.

## ⚙️ Tecnologias

- Python 3.x
- Requests
- Grafana HTTP API
- Cisco DNA Center API

## 🚀 Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/dnac-grafana-integration.git
cd dnac-grafana-integration
