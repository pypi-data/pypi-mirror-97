import json
import os, os.path
import pathlib

import requests

from . import characters_ssbu

# =============================================================================
API_HOST = "api.challonge.com"
API_ENDPOINT = "v1"
API_SCHEME = "https"
API_URL = "{scheme}://{host}/{endpoint}".format(
        scheme = API_SCHEME,
        host = API_HOST,
        endpoint = API_ENDPOINT,
        )

CHARACTERS = { c.smashggid : c.name for c in characters_ssbu.EVERYONE }

PLAYERSKINS = {}


# =============================================================================
def get_participants( api_key, tournament, proxy = None, log = None ):
    
    payload = {
            "api_key": api_key,
            }
    headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

    rv = requests.get(
            "{url}/{tournament}/participants.json".format(
                url = API_URL,
                tournament = tournament,
                )
            json.dumps(payload).encode("utf-8"),
            headers = headers,
            proxies = { "http": proxy, "https": proxy},
            )

    try:
        rv_json = rv.json()
    except Exception as e:
        log.error("HTTP request failed")
        log.error(e)
        log.debug(e, exc_info=True)
        log.debug(rv)

    return rv_json
