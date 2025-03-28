#!/bin/bash
  while true; do
      if ! systemctl is-active --quiet nginx; then
          echo "⚠️ Nginx caiu! Reiniciando e enviando notificação..."
          echo "$(TZ=America/Sao_Paulo date '+%Y-%m-%d %H:%M:%S') - O site caiu e foi reiniciado" >> /var/log/nginx_monitoramento.log
          python3 /usr/local/bin/telegram_notify.py
      fi
      sleep 10  # Verifica a cada 10s
  done 
