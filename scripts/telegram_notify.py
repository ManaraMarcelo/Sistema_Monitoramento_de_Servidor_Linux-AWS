import requests

# Configurações do Telegram
TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"
MESSAGE = "ALERTA: O Nginx caiu e está sendo reiniciado!"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    response = requests.post(url, data=data)
    return response.json()

# Teste o envio da mensagem
if __name__ == "__main__":
    result = send_telegram_message(MESSAGE)
    print(result)  # Verifica se foi enviado corretamente
