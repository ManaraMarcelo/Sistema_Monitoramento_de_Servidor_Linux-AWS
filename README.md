# Linux + AWS - Monitoramento e Automação

## 📌 Sobre o Projeto
Este projeto foi desenvolvido para implementar um ambiente automatizado de monitoramento e recuperação do serviço **NGINX** em uma instância **AWS EC2** rodando **Ubuntu Linux**. Ele inclui notificações via **Telegram** e armazenamento de logs para análise posterior.

---

## 📜 Menu
- [🚀 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [⚙️ Pré-requisitos](#️-pré-requisitos)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [📌 Configuração do NGINX](#-configuração-do-nginx)
- [📡 Monitoramento e Notificação](#-monitoramento-e-notificação)
- [📊 Armazenamento de Logs](#-armazenamento-de-logs)
- [🎯 Próximos Passos](#-próximos-passos)

---

## 🚀 Tecnologias Utilizadas
- **AWS EC2** (Ubuntu 22.04)
- **NGINX** (Web Server)
- **SystemD** (Gerenciamento de serviços)
- **Python** (Notificações via Telegram)
- **Shell Script** (Automação e logs)

---

## ⚙️ Pré-requisitos
Antes de começar, você precisará ter:
- Uma instância EC2 rodando Ubuntu
- Acesso **SSH** à instância
- Um **bot do Telegram** configurado para receber notificações
- NGINX instalado

---

## 📂 Estrutura do Projeto
```bash
/
├── /scripts
│   ├── monitor_nginx.sh       # Script para monitorar e reiniciar o NGINX
│   ├── notify_telegram.py      # Script Python para enviar notificações
│   ├── logs.txt               # Arquivo de log dos eventos
├── /systemd
│   ├── nginx-monitor.service   # Serviço systemd para o monitoramento automático
```

---

## 📌 Configuração do NGINX
1. Instale o **NGINX**:
   ```bash
   sudo apt update && sudo apt install -y nginx
   ```
2. Inicie e habilite o serviço:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

---

## 📡 Monitoramento e Notificação
Criamos um script que monitora o status do NGINX e reinicia o serviço se necessário. Caso o serviço falhe, ele envia uma notificação via Telegram.

### 🔧 Configuração do Monitoramento
Crie o script `/scripts/monitor_nginx.sh`:
```bash
#!/bin/bash
if ! systemctl is-active --quiet nginx; then
    echo "$(date) - NGINX caiu! Reiniciando..." >> /scripts/logs.txt
    systemctl restart nginx
    python3 /scripts/notify_telegram.py "NGINX caiu e foi reiniciado!"
fi
```

Dê permissão de execução:
```bash
chmod +x /scripts/monitor_nginx.sh
```

---

## 📊 Armazenamento de Logs
Todos os eventos são registrados no arquivo `logs.txt` para análise futura:
```bash
echo "$(date) - Mensagem de log" >> /scripts/logs.txt
```

---

## 🎯 Próximos Passos
- [ ] Adicionar suporte a envio de logs via Telegram
- [ ] Criar um painel de monitoramento
- [ ] Implementar métricas via Prometheus

---

📩 **Dúvidas ou sugestões?** Entre em contato! 🚀


