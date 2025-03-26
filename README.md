# Sistema de Monitoramento de Servidor [Linux e AWS]

Este projeto envolve a configuração de uma instância EC2 na AWS com Nginx, automação de monitoramento e notificações via Telegram.
Sempre em casos de queda do servidor web, após o tempo determinado no script ele irá retornar ativo e enviará uma notificação via Telegram para o seu dispositivo conectado (desktop e/ou mobile), alertando sobre a queda e notificando o retorno do servidor.

## 📌 Índice
1. [Criação da VPC](#1️⃣-criação-da-vpc)
2. [Configuração do Security Group](#2️⃣-configuração-do-security-group)
3. [Criação da Instância](#3️⃣-criação-da-instância)
4. [Configuração da Chave de Acesso](#4️⃣-configuração-da-chave-de-acesso)
5. [Conexão à Instância](#5️⃣-conexão-à-instância)
6. [Instalação de Dependências](#6️⃣-instalação-de-dependências)
7. [Ativação do Nginx](#7️⃣-ativação-do-nginx)
8. [Modificação da Página Web](#8️⃣-modificação-da-página-web)
9. [Configuração do SystemD](#9️⃣-configuração-do-systemd)
10. [Criação do Bot do Telegram](#🔟-criação-do-bot-do-telegram)
11. [Criação do Script de Monitoramento](#1️⃣1️⃣-criação-do-script-de-monitoramento)
12. [Logs e Monitoramento](#1️⃣2️⃣-logs-e-monitoramento)
13. [Teste Final](#1️⃣3️⃣-teste-final)
14. [Conclusão](#✅-conclusão)

## 1️⃣ Criação da VPC
Criar uma VPC de sua preferência. No meu caso criei uma com 3 subnets publicas e 3 privadas:

![Rotas de VPC](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/VPC.png)

## 2️⃣ Configuração do Security Group
- Criar um Security Group com três partições: SSH, HTTP e CUSTOM TCP(caso queira liberar alguma porta específica).
- Liberar portas HTTP(80) e SSH(22) privadas apenas para o seu IP.
- Após a aplicação estar pronta, liberar apenas HTTP para o público, pois o SSH fica para acesso administrativo;.

![Security Group](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/SecurityGroup.png)

## 3️⃣ Criação da Instância
- Criar um par de chaves para acesso.
- Habilitar IP público.
- Selecionar o Security Group correto.
- Escolher a sub-rede pública da VPC.

![Imagem Ubuntu Selecionada](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/AMI%20ubuntu.jpg)

![Criação Key Pair](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/Key%20Pair.jpg)

![Resumo e Configs](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/All%20resume%20Instance.jpg)

![Memória da Instância](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/Instance%20space.jpg)     

Não é necessário mexer em detalhes avançados.

## 4️⃣ Configuração da Chave de Acesso
Mover a chave privada baixada para `/home/"seuUsuario"/.ssh/` ou um diretório de sua preferência e definir permissões:
```sh
chmod 400 /home/"seuUsuario"/.ssh/"sua-chave".pem
```

## 5️⃣ Conexão à Instância
Conectar via SSH usando o comando à seguir:
```sh
ssh -i /home/"seuUsuario"/.ssh/"sua-chave.pem" ubuntu@IP_DA_INSTÂNCIA
```
Ou copiando o comando gerado dentro da aba 'conect to instance' na AWS:

![Atalho para conectar à instância](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/connect%20SSH.png)

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

![Tela Inicial Nginx](https://github.com/ManaraMarcelo/Sistema_Monitoramento_de_Servidor_Linux-AWS/blob/main/images/welcomeToNginx.jpg)

- instale o python também se não tiver instalado ainda.

## 8️⃣ Modificação da Página Web
Para estilizar a página web podemos fazer os seguintes passos: 

O diretório padrão para arquivos da web no Ubuntu é:
```sh
cd /var/www/html
```
onde nesse diretório podemos adicionar nosso 'index.html' e 'style.css' ou mais arquivos como preferir.
- Minha pagina = [index.html](scripts/index.html).
- Minha estilização = [style.css](scripts/styles.css).

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
 - Pesquise por '@BotFather' no buscar e crio um bot a partir dele.

Para obter o chat ID acesse o enderço a seguir alterando o seu TOKEN:
```sh
https://api.telegram.org/bot<TOKEN>/getUpdates
```
O ID estará no JSON retornado:
```json
"chat":{"id":"seuChatID_emNumeros","first_name":"seuNome","last_name":"seuSobrenome","type":"private"}
```

## 1️⃣1️⃣ Criação do Script de Monitoramento
Criar script Python para notificações em `/usr/local/bin/telegram_notify.py`.
- Meu código Python = [telegram_notify.py](scripts/telegram_notify.py).

Criar script Bash para monitoramento em `/usr/local/bin/monitor_nginx.sh` e conceder permissão de execução:
- Meu código Bash = [monitor_nginx.sh](scripts/monitor_nginx.sh).

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
Caso um dia precise remover o novo serviço:
```sh
sudo systemctl disable monitor_nginx
sudo rm /etc/systemd/system/monitor_nginx.service
sudo rm /usr/local/bin/monitor_nginx.sh
```

## 1️⃣2️⃣ Logs e Monitoramento
O próprio codigo Bash feito anteriormente já cuida desse processo com a seguinte linha:
```sh
echo "$(TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S') - O site caiu e foi reiniciado" >> /var/log/nginx_monitoramento.log
```
Os logs criados são armazenados no diretório: (/var/log/nginx_monitoramento.log)
Para verificar os logs gerados pelo script feito basta usar o seguinte comando 
```sh
sudo cat /var/log/nginx_monitoramento.log
```

Caso deseje verificar os logs do serviço criado com mais detalhes:
```sh
sudo journalctl -u monitor_nginx --since "1 hour ago"
```
Verificar logs do próprio Nginx:
```sh
tail -f /var/log/nginx/access.log
```

## 1️⃣3️⃣ Teste Final
Agora, após feitas todas as configurações anteriores, resta apenas testar se está funcionando:
- derrube o sistema nginx com:
```sh
sudo pkill -9 nginx
```
- após isso o servidor web deve cair e retornar uma notificação pelo telegram.

## ✅ Conclusão
Este projeto demonstra a implementação de um servidor web robusto na AWS, utilizando Linux, Nginx e automação para garantir alta disponibilidade e monitoramento eficiente. Além disso, integramos um sistema de notificações via Telegram, permitindo alertas rápidos sempre que houver quedas no serviço.

Através desse projeto, foi possível explorar conceitos essenciais de infraestrutura em nuvem, automação e monitoramento, tornando o ambiente mais seguro e confiável. O uso de SystemD e logs personalizados garante uma administração eficiente, enquanto o bot do Telegram proporciona uma camada extra de controle e resposta rápida a incidentes.

Se você chegou até aqui, espero que este projeto tenha sido útil para você! Caso tenha sugestões, dúvidas ou melhorias, fique à vontade para contribuir ou entrar em contato. 🚀

🔗 Contato: zmarcelo2018@gmail.com                                                                                 
💡 Sugestões e melhorias são sempre bem-vindas!
