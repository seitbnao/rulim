
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def obter_cardapio(data, tipo):
    url = 'https://www.sar.unicamp.br/RU/view/site/cardapio.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    blocos = soup.find_all("div", class_="panel panel-default")
    data_str = data.strftime('%d/%m/%Y')
    tipo = tipo.lower()

    for bloco in blocos:
        if data_str in bloco.text and tipo in bloco.text.lower():
            return bloco.get_text(separator="\n").strip()

    return f"Desculpe, não encontrei o {tipo} de {data_str}."

def lambda_handler(event, context):
    intent = event['request']['intent']['name']
    agora = datetime.now()

    if intent == 'RefeicaoDiaIntent':
        tipo = 'almoço' if agora.hour < 14 else 'jantar'
        data = agora
    elif intent == 'RefeicaoAmanhaIntent':
        tipo = 'almoço'
        data = agora + timedelta(days=1)
    else:
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Não entendi sua pergunta.'
                },
                'shouldEndSession': True
            }
        }

    resposta = obter_cardapio(data, tipo)

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': resposta
            },
            'shouldEndSession': True
        }
    }
