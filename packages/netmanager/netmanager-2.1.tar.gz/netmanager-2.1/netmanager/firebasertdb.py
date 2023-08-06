from netmanager import NetRequest


class FirebaseRTDB:
    def __init__(self, database_url):
        self.url = database_url + "/"

    def get(self, path='/'):
        url = self.url + path + "/.json"
        response = NetRequest(url)
        return response.result

    def set(self, path='/', data='null'):
        url = self.url + path + ".json"
        response = NetRequest(url, method='PUT', data=str(data))
        return response.status
