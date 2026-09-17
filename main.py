from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "36412578"
WHATSAPP_TOKEN = "EAAVwyNiGZADgBSmbA1Luh4C4OoGeYxH2GUfUdypPQQOYBGGVUYyzv4YlWGwS0z3yA1sQI5dTUW5lzzH7P5Jad3oiZAsn7klLzzsUzMM6g3IH2fnjdqSHqlxfUMnCyfToMvTDQkcKSS3DgqOTv6JZCPg571Yh214A2t7dN957lVukfqYqXSyKvN8q67EMzVknftcZBMAVYpS0KAIUgcPM9IHbxBqwgFfEQZBaTKarQMrk37FHA5GFK3h6K2BCuTKOx3jErd7R6NmJy1ZAjjbpJY"
PHONE_NUMBER_ID ="1371235692729572"

@app.route("/", methods=['GET'])
def home():
 return "Hello, World!"

@app.route("/webhook", methods=['GET'])
def verify_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Forbidden", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    if 'object' in data and 'entry' in data:
        for entry in data['entry']:
            for change in entry['changes']:
                if 'value' in change and 'messages' in change['value']:
                    for message in change['value']['messages']:
                        sender = message['from']
                        text = message['text']['body'].lower()
                        
                        responses = {"hi": "Hello!", "bye": "Goodbye!"}
                        reply = responses.get(text, "আমি বুঝতে পারিনি")
                        
                        send_whatsapp_message(sender, reply)
                        
    return jsonify({"status": "received"}), 200

def send_whatsapp_message(recipient, text):
    url = f"https://graph.facebook.com/v12.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": recipient, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(port=5000)
