import requests, json
from requests_oauthlib import OAuth1
from getpass import getpass

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
API_URL = TESLA_API_BASE_URL + 'api/1'


def get_new_token(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, email,password):
        request_data = {
            'grant_type': 'password',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'email': email,
            'password': password
        }

        response = requests.post(TOKEN_URL, data=request_data)
        response_json = response.json()

        if 'response' in response_json:
            raise AuthenticationError(response_json['response'])

        return response_json



TESLA_CLIENT_ID="81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
TESLA_CLIENT_SECRET="c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"

#Read in your username and password from commandline
# USERNAME = input('Username: ')
# PASSWORD = getpass('Password: ')
# auth = get_new_token(TESLA_CLIENT_ID,TESLA_CLIENT_SECRET,USERNAME,PASSWORD)

# header = {'Authorization': 'Bearer {}'.format(auth["access_token"])}
header = {'Authorization': 'Bearer 21f7983ae80df8b9141fa28806c611d4b5d1400461e13de2e88df7497a886f9d'}
print(header)

response = requests.get('{}/{}'.format(API_URL, "products"), headers=header)
response_json = response.json()
for product in response_json["response"]:
    if "energy_site_id" in product:
        print(product)
        url = '{}/{}'.format(API_URL, "energy_sites/"+str(product["energy_site_id"])+"/calendar_history")
        print(url)
        # print(header)
        response = requests.get(url, headers=header)
        print(response)
        if not 404 == response.status_code:
            response_json = response.json()
            print(response_json)
        else:
            print('Not Found.')