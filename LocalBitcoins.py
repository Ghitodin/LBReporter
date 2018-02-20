# lbcapi wrapper
from lbcapi import api


class LocalBitcoins:

    @staticmethod
    def get_user(hmac, hmac_secret):
        if hmac == '' or hmac_secret == '':
            raise ValueError("Wrong hmac or hmac secret")

        conn = api.hmac(hmac, hmac_secret)
        answer = conn.call('GET', '/api/myself/').json()

        # TODO: need to parse answer and construct User object:
        if answer is None:
            print("Api error!")
        else:
            print(answer)
