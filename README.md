# Projeto de Deploy com Linux e AWS

Este projeto envolve a configuração de uma instância EC2 na AWS com Nginx, automação de monitoramento e notificações via Telegram.

## 📌 Índice
1. [Criação da VPC](#criação-da-vpc)
2. [Configuração do Security Group](#configuração-do-security-group)
3. [Criação da Instância](#criação-da-instância)
4. [Configuração da Chave de Acesso](#configuração-da-chave-de-acesso)
5. [Conexão à Instância](#conexão-à-instância)
6. [Instalação de Dependências](#instalação-de-dependências)
7. [Ativação do Nginx](#ativação-do-nginx)
8. [Modificação da Página Web](#modificação-da-página-web)
9. [Configuração do SystemD](#configuração-do-systemd)
10. [Criação do Bot do Telegram](#criação-do-bot-do-telegram)
11. [Criação do Script de Monitoramento](#criação-do-script-de-monitoramento)
12. [Logs e Monitoramento](#logs-e-monitoramento)

## 1️⃣ Criação da VPC
Criar uma VPC com três sub-redes separadas.

## 2️⃣ Configuração do Security Group
- Criar um Security Group com três partições.
- Liberar portas HTTP e SSH privadas apenas para o seu IP.
- Após a aplicação estar pronta, liberar apenas HTTP.

## 3️⃣ Criação da Instância
- Criar um par de chaves para acesso.
- Habilitar IP público.
- Selecionar o Security Group correto.
- Escolher a sub-rede pública da VPC.

## 4️⃣ Configuração da Chave de Acesso
Mover a chave para `/home/marcelomanara/.ssh/` e definir permissões:
```sh
chmod 400 /home/marcelomanara/.ssh/sua-chave.pem
```

## 5️⃣ Conexão à Instância
Conectar via SSH usando:
```sh
ssh -i /home/marcelomanara/.ssh/sua-chave.pem ubuntu@IP_DA_INSTÂNCIA
```

## 6️⃣ Instalação de Dependências
```sh
sudo apt-get update -y
sudo apt-get install iptables nginx -y
```

## 7️⃣ Ativação do Nginx
```sh
sudo systemctl start nginx
sudo systemctl enable nginx
```
Acesse via IP público da instância no navegador.

## 8️⃣ Modificação da Página Web
O diretório padrão para arquivos da web no Ubuntu é:
```sh
cd /var/www/html
```

## 9️⃣ Configuração do SystemD
Editar o serviço do Nginx para garantir reinicialização automática:
```sh
sudo nano /usr/lib/systemd/system/nginx.service
```
Adicionar as linhas em `[Service]`:
```
Restart=always
RestartSec=7s
```
Recarregar e reiniciar o serviço:
```sh
sudo systemctl daemon-reload
sudo systemctl restart nginx
```
Testar a configuração:
```sh
sudo systemctl status nginx
sudo pkill -9 nginx
sudo systemctl status nginx
```

## 🔟 Criação do Bot do Telegram
Criar um bot via @BotFather e obter o token.

Para obter o chat ID:
```sh
https://api.telegram.org/bot<TOKEN>/getUpdates
```
O ID estará no JSON retornado:
```json
"chat":{"id":7596659083,"first_name":"Marcelo","last_name":"Manara","type":"private"}
```

## 1️⃣1️⃣ Criação do Script de Monitoramento
Criar script Python para monitoramento e notificações em `/usr/local/bin/telegram_notify.py`.

Criar script Bash para monitoramento em `/usr/local/bin/monitor_nginx.sh` e conceder permissão de execução:
```sh
sudo chmod +x /usr/local/bin/monitor_nginx.sh
```
Criar serviço SystemD:
```sh
sudo nano /etc/systemd/system/monitor_nginx.service
```
Adicionar:
```
[Unit]
Description=Monitoramento do Nginx
After=network.target

[Service]
ExecStart=/usr/local/bin/monitor_nginx.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```
Habilitar e iniciar o serviço:
```sh
sudo systemctl enable monitor_nginx
sudo systemctl start monitor_nginx
sudo systemctl status monitor_nginx
```
Para remover:
```sh
sudo systemctl disable monitor_nginx
sudo rm /etc/systemd/system/monitor_nginx.service
sudo rm /usr/local/bin/monitor_nginx.sh
```

## 1️⃣2️⃣ Logs e Monitoramento
Para armazenar logs quando o site cair:
```sh
echo "$(date '+%Y-%m-%d %H:%M:%S') - Site caiu" >> /var/log/nginx_monitoramento.log
```
Verificar logs do serviço:
```sh
sudo journalctl -u monitor_nginx --since "1 hour ago"
```
Verificar logs do Nginx:
```sh
tail -f /var/log/nginx/access.log
```

