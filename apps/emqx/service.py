import requests
from django.conf import settings


API_ROOT = settings.EMQX_API_URL

API = {
    "disconnect": "/connetions/"
}

API_ID = settings.EMQX_API_ID
API_SECRET = settings.EMQX_API_SECRET


def get_url(name):
    return API_ROOT + API.get(name)


class EmqxService(object):
    @classmethod
    def disconnect_client(cls, client_id):
        api_url = "{url}{client_id}".format(url=get_url("disconnect"),
                                            client_id=client_id)

        return requests.delete(api_url, auth=(API_ID, API_SECRET))

