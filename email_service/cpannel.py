import requests

CPANEL_USER = "cpanelusername"
CPANEL_TOKEN = "your_api_token"
CPANEL_HOST = "https://yourdomain.com:2083"

def create_email(email, password):
    url = f"{CPANEL_HOST}/execute/Email/add_pop"

    headers = {
        "Authorization": f"cpanel {CPANEL_USER}:{CPANEL_TOKEN}"
    }

    payload = {
        "email": email,
        "domain": "natdemy.in",
        "password": password,
        "quota": 500
    }

    response = requests.post(url, headers=headers, data=payload)

    return response.json()