from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.get("/")
def home():
    return {"ok": True, "msg": "AcheiBarato API rodando"}

@app.get("/buscar")
def buscar():
    produto = request.args.get("produto", "").strip()

    if not produto:
        return jsonify([])

    url = "https://api.mercadolibre.com/sites/MLB/search"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }

    params = {
        "q": produto,
        "limit": 10
    }

    resposta = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=20
    )

    dados = resposta.json()

    resultados = []
    for item in dados.get("results", []):
        resultados.append({
            "loja": "Mercado Livre",
            "produto": item.get("title"),
            "preco": item.get("price"),
            "link": item.get("permalink"),
            "imagem": item.get("thumbnail")
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
