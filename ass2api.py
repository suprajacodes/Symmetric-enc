import warnings
warnings.filterwarnings("ignore")
import time, base64, json, requests, argparse, os
from flask import Flask, request as flask_request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

BASE_URL="https://amer.smartkey.io"

app = Flask(__name__)
CORS(app)

def request(endpoint, method, body={}, headers = {}):
    try:
        body = json.dumps(body)
        print(f"Requesting {method} {BASE_URL + endpoint} with headers {headers} and body {body}")
        response = requests.request(method, BASE_URL + endpoint, headers=headers, data=body)
        response.raise_for_status()  # Raises a HTTPError if the response contains an HTTP status code that indicates an error
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        if response is not None:
            print(f'Response content: {response.text}')
        return None
    else:
        return response.json()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = flask_request.get_json()
    toBeEncrypted = data['text']
    apiKey = os.getenv('API_KEY')
    headers = {'Authorization': 'Basic ' + apiKey}
    print(f'Received request to encrypt text: {toBeEncrypted}')
    print(f'Using API key: {apiKey}')
    print('Creating an AES key...', end='')
    aesKey = request('/crypto/v1/keys', 'POST', body={ "name": f"Test_{time.time()}", "obj_type": "Aes", "key_size": 256 }, headers=headers)
    if aesKey is None:
        print('Failed to create AES key.')
        return jsonify({"error": "Failed to create AES key. Please check your API key and try again."}), 403
    print('\033[92m' + '[OK]' + '\033[0m')

    print('Encrypting data...', end='')
    encryptedData = request('/crypto/v1/encrypt', 'POST', 
                                    body={ 
                                        "alg": "Aes",
                                        "mode": "CBC",
                                        "plain": base64.b64encode(toBeEncrypted.encode('ascii')).decode('ascii'), 
                                        "key": {
                                            "kid": aesKey['kid'],
                                        }}, headers=headers)
    if encryptedData is None:
        print('Failed to encrypt data.')
        return jsonify({"error": "Failed to encrypt data. Please try again."}), 500
    print('\033[92m' + '[OK]' + '\033[0m', end='\n\n\n')

    return jsonify({
        "cipher": encryptedData['cipher'],
        "iv": encryptedData['iv']
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Encrypt a string")
    parser.add_argument("--text", help="The string to be encrypted", default="Hello world")
    args = parser.parse_args()
    toBeEncrypted = args.text
    apiKey = os.getenv('API_KEY')
    if apiKey is None:
        print('\033[91m' + 'ERROR:' + '\033[0m' + ' API_KEY environment variable is not set')
        exit(1)
    headers = {'Authorization': 'Basic ' + apiKey}
    print(f'Using API key from environment: {apiKey}')
    print('Creating an AES key...', end='')
    aesKey = request('/crypto/v1/keys', 'POST', body={ "name": f"Test_{time.time()}", "obj_type": "Aes", "key_size": 256 }, headers=headers)
    if aesKey is None:
        print('\033[91m' + 'ERROR:' + '\033[0m' + ' Failed to create AES key. Please check your API key and try again.')
        exit(1)
    print('\033[92m' + '[OK]' + '\033[0m')

    print('Encrypting data...', end='')
    encryptedData = request('/crypto/v1/encrypt', 'POST', 
                                    body={ 
                                        "alg": "Aes",
                                        "mode": "CBC",
                                        "plain": base64.b64encode(toBeEncrypted.encode('ascii')).decode('ascii'), 
                                        "key": {
                                            "kid": aesKey['kid'],
                                        }}, headers=headers)
    if encryptedData is None:
        print('\033[91m' + 'ERROR:' + '\033[0m' + ' Failed to encrypt data. Please try again.')
        exit(1)
    print('\033[92m' + '[OK]' + '\033[0m', end='\n\n\n')

    print('\033[1m' + 'Encrypted data' + '\033[0m')
    print('\033[94m' + f"Cipher: {encryptedData['cipher']}" + '\033[0m')
    print('\033[94m' + f"IV: {encryptedData['iv']}" + '\033[0m')

    app.run(host='0.0.0.0', port=5000)
