import warnings
warnings.filterwarnings("ignore")
import time, base64, json, requests, argparse, os


API_KEYS=os.getenv('API_KEYS')
BASE_URL="https://amer.smartkey.io"

def request(endpoint, method, body={}, headers = {}):
    headers['Authorization'] = 'Basic  ' + API_KEYS
    try:
        body = json.dumps(body)
        response = requests.request(method, BASE_URL + endpoint, headers=headers, data=body)
        response.raise_for_status()  # Raises a HTTPError if the response contains an HTTP status code that indicates an error
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e} {response.text}')
        return None
    else:
        return response.json()

if __name__ == '__main__':
    if (API_KEYS is None):
        print('\033[91m' + 'ERROR:' + '\033[0m' + ' API_KEYS environment variable is not set')
        exit(1)
    parser = argparse.ArgumentParser(description="Encrypt a string")
    parser.add_argument("--text", help="The string to be encrypted", default="Hello world")
    args = parser.parse_args()
    toBeEncrypted = args.text
    print('Creating an AES key...', end='')
    aesKey = request('/crypto/v1/keys', 'POST', body={ "name": f"Test_{time.time()}", "obj_type": "Aes", "key_size": 256 })
    print('\033[92m' + '[OK]' + '\033[0m')

    print('Encrypting data...', end='')
    encryptedData = request('/crypto/v1/encrypt', 'POST', 
                                    body={ 
                                        "alg": "Aes",
                                        "mode": "CBC",
                                        "plain": base64.b64encode(toBeEncrypted.encode('ascii')).decode('ascii'), 
                                        "key": {
                                            "kid": aesKey['kid'],
                                        }})
    print('\033[92m' + '[OK]' + '\033[0m', end='\n\n\n')

    print('\033[1m' + 'Encrypted data' + '\033[0m')
    print('\033[94m' + f"Cipher: {encryptedData['cipher']}" + '\033[0m')
    print('\033[94m' + f"IV: {encryptedData['iv']}" + '\033[0m')
