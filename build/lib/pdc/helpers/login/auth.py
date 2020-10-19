import requests
from pdc import settings

class Api():

    def pdcLoginCheck(token):
        loginCheck = False
        try:
            response = requests.get(settings.PDC_SWARM_AUTHORIZATOR_API + "isauthenticated/?token=" + token)
            if response.json()["authenticated"] == "true":
                loginCheck = True
        except:
            loginCheck = False
        return loginCheck

    def pdcGetUsername(token):
        response = requests.get(settings.PDC_SWARM_AUTHORIZATOR_API + "getuser/?token=" + token)
        return response.json()["username"]
