import requests
import base64
import json
from datetime import datetime
import pytz
import qrcode
from io import BytesIO

# OAuth 2.0 API endpoint
OAUTH_URL = "https://openapi-sandbox.kasikornbank.com/v2/oauth/token"
# QR Code generation API endpoint
QR_URL = "https://openapi-sandbox.kasikornbank.com/v1/qrpayment/request"

# Your credentials
CONSUMER_ID = "suDxvMLTLYsQwL1R0L9UL1m8Ceoibmcr"
CONSUMER_SECRET = "goOfPtGLoGxYP3DG"

# Partner information
PARTNER_ID = "PTR1051673"
PARTNER_SECRET = "d4bded59200547bc85903574a293831b"
MERCHANT_ID = "KB102057149704"

# Get current time in Bangkok timezone
bangkok_tz = pytz.timezone('Asia/Bangkok')
current_time = datetime.now(bangkok_tz)

def generate_auth_header(consumer_id, consumer_secret):
    """Generate the Authorization header for OAuth 2.0"""
    credentials = f"{consumer_id}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def get_access_token():
    """Get an access token using OAuth 2.0 Client Credentials flow"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": generate_auth_header(CONSUMER_ID, CONSUMER_SECRET),
        "x-test-mode": "true",
        "env-id": "OAUTH2"
    }
    
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(OAUTH_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error getting access token: {response.status_code}")
        print(response.text)
        return None

def generate_qr_code(access_token, amount, reference1, reference2=None, reference3=None, reference4=None, metadata=None):
    """Generate a Thai QR Code"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "x-test-mode": "true",
        "env-id": "QR002"
    }
    
    data = {
        "partnerTxnUid": "PARTNERTEST0001",
        "partnerId": PARTNER_ID,
        "partnerSecret": PARTNER_SECRET,
        "requestDt": current_time.isoformat(),
        "merchantId": MERCHANT_ID,
        "qrType": "3",
        "txnAmount": str(amount),
        "txnCurrencyCode": "THB",
        "reference1": reference1,
        "reference2": reference2,
        "reference3": reference3,
        "reference4": reference4,
        "metadata": metadata
    }
    
    response = requests.post(QR_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error generating QR code: {response.status_code}")
        print(response.text)
        return None

def create_qr_image(qr_data):
    """Create a QR code image from the provided data"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def save_qr_image(img, filename="qr_code.png"):
    """Save the QR code image to a file"""
    img.save(filename)
    print(f"QR code image saved as {filename}")

def main():
    print("Getting access token...")
    access_token = get_access_token()
    
    if access_token:
        print("Access token received successfully!")
        
        amount = float(input("Enter the amount for the QR code: "))
        reference1 = input("Enter Reference 1 (e.g., INV001): ")
        reference2 = input("Enter Reference 2 (optional): ") or None
        reference3 = input("Enter Reference 3 (optional): ") or None
        reference4 = input("Enter Reference 4 (optional): ") or None
        metadata = input("Enter metadata (optional, e.g., 'Item1 50.00, Item2 30.50'): ") or None
        
        print("Generating QR code...")
        qr_response = generate_qr_code(access_token, amount, reference1, reference2, reference3, reference4, metadata)
        
        if qr_response:
            print("QR code generated successfully!")
            print(f"QR Code data: {qr_response.get('qrCode')}")
            
            # Create and save QR code image
            qr_data = qr_response.get('qrCode')
            if qr_data:
                qr_image = create_qr_image(qr_data)
                save_qr_image(qr_image)
            else:
                print("QR code data not found in the response.")
        else:
            print("Failed to generate QR code.")
    else:
        print("Failed to get access token.")

if __name__ == "__main__":
    main()