# Projeto de Deploy com Linux e AWS

Este projeto envolve a configuração de uma instância EC2 na AWS com Nginx, automação de monitoramento e notificações via Telegram.
Sempre em casos de queda do servidor web, após o tempo determinado no script ele irá retornar ativo e enviará uma notificação via Telegram para o seu dispositivo conectado (desktop e/ou mobile), alertando sobre a queda e notificando o retorno do servidor.

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
Criar uma VPC de sua preferência. No meu caso criei uma com 3 subnets publicas e 3 privadas:

---Imagem---

## 2️⃣ Configuração do Security Group
- Criar um Security Group com três partições: SSH, HTTP e CUSTOM TCP(caso queira liberar alguma porta específica).
- Liberar portas HTTP(80) e SSH(22) privadas apenas para o seu IP.
- Após a aplicação estar pronta, liberar apenas HTTP para o público, pois o SSH fica para acesso administrativo;.

--- IMAGEM ---

## 3️⃣ Criação da Instância
- Criar um par de chaves para acesso.
- Habilitar IP público.
- Selecionar o Security Group correto.
- Escolher a sub-rede pública da VPC.

--- IMAGEM ---

## 4️⃣ Configuração da Chave de Acesso
Mover a chave privada baixada para `/home/<seuUsuario>/.ssh/` ou um diretório de sua preferência e definir permissões:
```sh
chmod 400 /home/<seuUsuario>/.ssh/<sua-chave>.pem
```

## 5️⃣ Conexão à Instância
Conectar via SSH usando o comando à seguir:
```sh
ssh -i /home/<seuUsuario>/.ssh/sua-chave.pem ubuntu@IP_DA_INSTÂNCIA
```
Ou copiando o comando gerado dentro da aba 'conect to instance' na AWS:

---IMAGEM---

## 6️⃣ Instalação de Dependências
Após ter se conectado com sucesso à instância, precisamos instalar o **NGINX**
```sh
sudo apt-get update -y
sudo apt-get install nginx -y
```

## 7️⃣ Ativação do Nginx
Após a instalação, o próximo passo é iniciar e testar o NGINX 
```sh
sudo systemctl start nginx
sudo systemctl enable nginx
```
Acesse via IP público da instância no navegador.
Se o serviço estiver funcionando corretamente, deve aparecer uma página web parecida com essa: 

---IMAGEM---

## 8️⃣ Modificação da Página Web
Para estilizar a página web podemos fazer os seguintes passos: 

O diretório padrão para arquivos da web no Ubuntu é:
```sh
cd /var/www/html
```
onde nesse diretório podemos adicionar nosso 'index.html' e 'style.css' ou mais arquivos como preferir.

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
Após o 'pkill' se você verificar o status e ele estiver ativo, quer dizer que está funcionando o systemd

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

