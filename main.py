from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

ACCESS_TOKEN = 'COLE_SEU_TOKEN_AQUI'
COMPANY_DOMAIN = 'SEUDOMINIO.amocrm.com'
FIELD_ID = 2060413

@app.route('/')
def home():
    return 'Webhook Kommo funcionando!'

@app.route('/recebe-webhook', methods=['POST'])
def recebe_webhook():
    dados = request.json
    try:
        lead = dados['leads']['update'][0]
        lead_id = lead['id']
        data_hoje = datetime.datetime.now().strftime('%Y-%m-%d')

        payload = {
            "update": [
                {
                    "id": lead_id,
                    "custom_fields_values": [
                        {
                            "field_id": FIELD_ID,
                            "values": [{"value": data_hoje}]
                        }
                    ]
                }
            ]
        }

        url = f'https://{COMPANY_DOMAIN}/api/v4/leads'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }

        r = requests.patch(url, json=payload, headers=headers)
        return jsonify({'status': 'ok', 'kommo': r.text}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
