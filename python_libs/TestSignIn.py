import requests


class TestSignIn(object):
    def __init__(self, url):
        self.url = url

    def sign_in(self, username, password):
        user_info = {'username': username,
                     'password': password
                     }
        response = requests.post(self.url, data=user_info)
        return response.json(),response.cookies['sessionid']
