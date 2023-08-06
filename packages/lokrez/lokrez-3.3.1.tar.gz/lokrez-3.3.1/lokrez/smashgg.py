import json
import os, os.path
import pathlib

import requests

from . import characters_ssbu

# =============================================================================
API_HOST = "api.smash.gg"
API_ENDPOINT = "gql/alpha"
API_SCHEME = "https"
API_URL = "{scheme}://{host}/{endpoint}".format(
        scheme = API_SCHEME,
        host = API_HOST,
        endpoint = API_ENDPOINT,
        )

CHARACTERS = { c.smashggid : c.name for c in characters_ssbu.EVERYONE }

GET_PLAYERDATA = lambda tag: {"tag": tag,}

# =============================================================================
# -----------------------------------------------------------------------------
class Player():
    """A Player, as registered by the smash.gg API, and their characters
    choices and placement in a tournament"""

    # -------------------------------------------------------------------------
    def __init__(
            self,
            id,
            prefix,
            gamerTag,
            placement,
            seeding,
            twitterHandle = None,
            chars = None
            ):
        self.id            = int(id) # actually intended to store an Entrant id
        self.prefix        = ( "" if prefix is None else prefix )
        self.gamerTag      = gamerTag
        self.placement     = int(placement)
        self.seeding       = int(seeding)
        self.twitterHandle = ( "" if twitterHandle is None else twitterHandle )

        try:
            self.playerdata = GET_PLAYERDATA(self.gamerTag)
        except:
            self.playerdata = {}

        # Check if there's a redirect in the players DB
        try:
            self.gamerTag = self.playerdata["tag"]
        except:
            pass

        # Prefix is superseeded by sponsors infos in DB
        try:
            self.prefix = self.playerdata["sponsor"]
        except:
            pass

        if chars is None:
            self.chars = {}
        else:
            self.chars = chars

    # -------------------------------------------------------------------------
    def add_character_selection(self, character, win):

        if type(character) != tuple:
            try:
                charname = CHARACTERS[character]
            except KeyError:
                charname = character # Unknown char -> sgg id

            try:
                skin = self.playerdata["skins"][charname]
            except KeyError:
                skin = "00" # default skin

            character = ( charname, skin )


        try:
            self.chars[character] += ( 1.01 if win else 1.00 )
            # This 1.01 / 1.00 tricks should hold until the player loses 101
            # matches with one character and wins 100 matches with another...
            # during one tournament.
        except KeyError:
            self.chars[character] = ( 1.01 if win else 1.00 )

    # -------------------------------------------------------------------------
    def get_mains(self):
        return [ cv[0] for cv in sorted(
            self.chars.items(),
            key = lambda cv: cv[1],
            reverse = True,
            ) ]

    # -------------------------------------------------------------------------
    def conf(self):

        # The char list looks like 'character1_skin1 (12.08), character2_skin2
        # (3.02)' where the number between parenthesis is the number of time
        # the character was played
        charslist = ", ".join( [ "{}_{} ({:.2f})".format(c,s,n) for (c,s),n in
            sorted( self.chars.items(), key = lambda cv: cv[1], reverse =
                True,) ])

        return """
[player {tag}]
tag: {tag}
team: {pfx}
seeding: {seed}
placement: {plc}
twitter: {twi}
characters: {charslist}""" \
            .format(
                    tag = self.gamerTag,
                    pfx = self.prefix,
                    seed = self.seeding,
                    plc = self.placement,
                    twi = self.twitterHandle,
                    charslist  = charslist,
                    )


    # -------------------------------------------------------------------------
    def __str__(self):
        # The char list looks like 'character1_skin1 (12.08), character2_skin2
        # (3.02)' where the number between parenthesis is the number of time
        # the character was played
        charslist = ", ".join( [ "{}_{} ({:.2f})".format(c,s,n) for (c,s),n in
            sorted( self.chars.items(), key = lambda cv: cv[1], reverse =
                True,) ])
        return "{plc}/ [{pfx}] {tag} -- {charslist}" \
                .format(
                    tag = self.gamerTag,
                    pfx = self.prefix,
                    plc = self.placement,
                    charslist  = charslist,
                        )

# -----------------------------------------------------------------------------
class Tournament():
    """A Tournament, as registered by the smash.gg API"""

    # -------------------------------------------------------------------------
    def __init__(
            self,
            id,
            name,
            slug,
            startAt,
            numEntrants,
            venueAddress = None,
            venueName = None,
            city = None,
            countryCode = None,
            hashtag = None,
            ):
        self.id           = id
        self.name         = name
        self.slug         = slug.split("/")[-1]
        self.startAt      = startAt
        self.numEntrants  = numEntrants
        self.venueAddress = venueAddress
        self.venueName    = venueName
        self.city         = city
        self.countryCode  = countryCode
        self.hashtag      = hashtag

    # -------------------------------------------------------------------------
    def conf(self):
        return """
[Tournament]
name: {name}
date: {date}
location: {loc} - {addr} ({city}, {ctry})
slug: {slug}
numEntrants: {nbe}""" \
            .format(
                    id = self.id,
                    name = self.name,
                    date = self.startAt,
                    loc = self.venueName,
                    addr = self.venueAddress,
                    city = self.city,
                    ctry = self.countryCode,
                    slug = self.slug,
                    nbe = self.numEntrants,
                    )

    # -------------------------------------------------------------------------
    def clean_name(self, name_seo_delimiter):

        if name_seo_delimiter is not None and name_seo_delimiter != "":
            self.name = self.name.split(name_seo_delimiter)[0].strip()

        return self

    # -------------------------------------------------------------------------
    def __str__(self):
        return "Tournament {name} ({date} at {loc}), {nbe} entrants" \
                .format(
                    id = self.id,
                    name = self.name,
                    date = self.startAt,
                    loc = self.venueName,
                    addr = self.venueAddress,
                    city = self.city,
                    ctry = self.countryCode,
                    slug = self.slug,
                    nbe = self.numEntrants,
                    )



# =============================================================================
def run_query(
        query_name,
        variables = {},
        token = "",
        proxy = None,
        query_dir = pathlib.Path("queries"),
        query_extension = "gql",
        api_url = API_URL,
        log = None,
        ):

    # Load query
    query_path = query_dir / "{}.{}".format(
            query_name,
            query_extension,
            )
    query  = ""

    with query_path.open("r") as query_file:
        query = query_file.read()

    # Build payload
    payload = {
            "query": query,
            "variables": json.dumps(variables),
            }

    # Build headers
    headers = {
            "Authorization": "Bearer {token}".format(token = token),
            "Accept": "application/json",
            "Content-Type": "application/json"
            }

    # Send the query
    try:
        log.debug("Sending query '{}' with variables:".format(query_name))
        log.debug(json.dumps(variables))
    except AttributeError:
        pass

    rv = requests.post(
            API_URL,
            json.dumps(payload).encode("utf-8"),
            headers = headers,
            proxies = {"http": proxy, "https": proxy},
            )

    try:
        rv_json = rv.json()
    except Exception as e:
        log.error("HTTP request failed")
        log.error(e)
        log.debug(e, exc_info=True)
        log.debug(rv)

    # Try to return the data, or log the error and return None
    try:
        log.debug("query complexity : {}" \
                .format(
                    rv_json["extensions"]["queryComplexity"],
                    ))
        return rv_json["data"]
    except KeyError:
        try:
            log.error("GraphQL error")
            log.error(rv_json)
        except AttributeError:
            pass
        return None

