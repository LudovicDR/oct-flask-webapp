from openai import AzureOpenAI
import json

g_messages = [
    {"role": "system", "content": "Tu es un assitant très efficace."},
    {"role": "user", "content": "Est-ce que tu es prêt à m'aider ?"},
    {"role": "assistant", "content": "Bien sûr, que puis-je faire pour te rendre service ?"}
]

def reset_messages():
    return [
        {"role": "system", "content": "Tu es un assitant très efficace."},
        {"role": "user", "content": "Est-ce que tu es prêt à m'aider ?"},
        {"role": "assistant", "content": "Bien sûr, que puis-je faire pour te rendre service ?"}
    ]

def generate_response(app, version):
    # Call API to generate response 
    client = AzureOpenAI(
        azure_endpoint = app.config["AZURE_OPENAI_ENDPOINT"], 
        api_key = app.config["AZURE_OPENAI_KEY"],  
        api_version = "2023-05-15"
    )
    model = "chat" if version == "3.5" else "gpt4"
    response = client.chat.completions.create(
        model = model,         # le nom du déploiement du modèle dans la ressource
        messages = g_messages, # la conversation
        stream = True)         # pour récupérer la réponse au fur et à mesure de sa génération
    collected_messages = []
    for event in response:
        if event.choices[0].delta.role == "assistant":
                yield "event:start\ndata: stream\n\n"
        if event.choices[0].delta.content is not None:
            response_message = event.choices[0].delta.content
            collected_messages.append(response_message)  # save the message
            json_data = json.dumps({"text": response_message})
            yield f"event:message\ndata: {json_data}\n\n"
    yield "event: end\ndata: stream\n\n"

    full_reply_content = ''.join([m for m in collected_messages])
    #print(f"{full_reply_content=}")
    g_messages.append({"role": "assistant", "content": full_reply_content })
