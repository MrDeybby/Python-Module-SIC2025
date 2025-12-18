import requests

res = requests.post(
    "http://localhost:8000/predict",
    json={
        "año": 2025,
        "mes": 1,
        "mes_pasado": 398.12,
        "region": "norte"
    }
)

print(res.json())
