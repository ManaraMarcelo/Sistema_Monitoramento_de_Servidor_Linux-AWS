import requests

# Configurações do Telegram
TOKEN = "8027561385:AAH0zECAzikdwUfiOOe_Ma2Pvev2do6Rpbw"
CHAT_ID = "7596659083"
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
