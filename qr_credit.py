import json
from datetime import datetime
import pytz

# API endpoint
QR_URL = "https://openapi-sandbox.kasikornbank.com/v1/qrpayment/request"

# Partner information
PARTNER_ID = "PTR1051673"
PARTNER_SECRET = "d4bded59200547bc85903574a293831b"
MERCHANT_ID = "KB102057149704"

def prepare_qr_credit_card_request(amount, reference1, reference2=None, reference3=None, reference4=None):
    """Prepare the headers and body for a QR Credit Card request"""
    
    # Get current time in Bangkok timezone
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(bangkok_tz)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer NMuSnuQv9Aa5JwYWNHGq2a35EYCe",
        "x-test-mode": "true",
        "env-id": "QR003"
    }
    
    body = {
        "partnerTxnUid": "PARTNERTEST0001-2",
        "partnerId": PARTNER_ID,
        "partnerSecret": PARTNER_SECRET,
        "requestDt": current_time.isoformat(),
        "merchantId": MERCHANT_ID,
        "qrType": "4",
        "txnAmount": f"{amount:.2f}",
        "txnCurrencyCode": "THB",
        "reference1": reference1,
        "reference2": reference2 or "HELLOWORLD",
        "reference3": reference3 or "INV001",
        "reference4": reference4 or "INV001"
    }
    
    return headers, body

def main():
    print("Preparing QR Credit Card request for Postman...")
    
    amount = float(input("Enter the amount for the QR Credit Card: "))
    reference1 = input("Enter Reference 1 (e.g., INV001): ")
    reference2 = input("Enter Reference 2 (optional, default is HELLOWORLD): ") or None
    reference3 = input("Enter Reference 3 (optional, default is INV001): ") or None
    reference4 = input("Enter Reference 4 (optional, default is INV001): ") or None
    
    headers, body = prepare_qr_credit_card_request(amount, reference1, reference2, reference3, reference4)
    
    print("\nAPI Endpoint:")
    print(QR_URL)
    
    print("\nHeaders for Postman:")
    print(json.dumps(headers, indent=2))
    
    print("\nBody for Postman:")
    print(json.dumps(body, indent=2))
    
    print("\nNOTE: Replace 'YOUR_ACCESS_TOKEN_HERE' in the Authorization header with your actual access token.")

if __name__ == "__main__":
    main()