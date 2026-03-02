import json
from datetime import datetime

from risk_engine import evaluate_transaction

if __name__ == "__main__":
    phone = "+99999991000"

    tx = {
        "transaction_id": "tx_demo_001",
        "timestamp": datetime.now().astimezone().isoformat(),
        "amount": 9500,
        "currency": "EUR",
        "type": "transfer",
        "channel": "mobile_app",
        "beneficiary_country": "HU",

        # Datos para KYC (los que tengáis en vuestro flujo real)
        "idDocument": "66666666q",
        "name": "Federica Sanchez Arjona",
        "givenName": "Federica",
        "familyName": "Sanchez Arjona",
        "address": "Tokyo-to Chiyoda-ku Iidabashi 3-10-10",
        "birthdate": "1978-08-22",
        "email": "abc@example.com",
        "country": "JP",

        # Number recycling
        "number_recycling_specified_date": "2024-10-31"
    }

    result = evaluate_transaction(phone, tx)

    # Esto es lo que consume el frontend
    print(json.dumps(result, indent=2, ensure_ascii=False))