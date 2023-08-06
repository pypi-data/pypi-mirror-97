import argparse
import configparser
import datetime
import html
import json
import logging
import pathlib
import requests
import sys
import urllib

import appdirs

from . import export
from . import resources
from . import smashgg
from . import version

# =============================================================================
__version__ = version.__version__
__license__ = version.__license__

ROOTDIR = pathlib.Path(__file__).absolute().parent

APPDIRS = appdirs.AppDirs(version.NAME, version.ENTITY)

LOG_DUMMY = logging.getLogger("dummy")
LOG_DUMMY.addHandler(logging.NullHandler())

DEFAULT_DIR_TEMPLATES = ROOTDIR / "templates"

# =============================================================================
def get_templates_list(
        dir_templates = DEFAULT_DIR_TEMPLATES,
        ):

    templates_list = []

    dir_templates_path = pathlib.Path(dir_templates)

    for potential_template in dir_templates_path.iterdir():

        if (potential_template / "template.svg.j2").is_file():
            templates_list.append(potential_template.name)

    return templates_list

# =============================================================================
def get_infos_from_url(
        url,
        token,
        options = {},
        outform = "dict",
        top = 8,
        proxy = None,
        log = LOG_DUMMY,
        ):

    url_parsed = urllib.parse.urlparse(url)

    if url_parsed.netloc not in [ "smash.gg" ]:
        raise ValueError("Unsupported domain name")
    if outform not in [ "dict", "lkrz" ]:
        raise ValueError("Unsupported outform")

    # -------------------------------------------------------------------------
    if url_parsed.netloc == "smash.gg":

        if (url_parsed.path.split("/")[1] != "tournament"):
            raise Exception("No tournament found in url {}".format(url_parsed.path.split("/")))

        # Get infos from smash.gg and write the config file
        tournament, top_players = getTournamentTop(
                id_or_slug = url_parsed.path.split("/")[2],
                get_prefixes = options.get("use_smashgg_prefixes", False),
                top = top,
                token = token,
                proxy = proxy,
                log = log,
                )

        if tournament is None or top_players is None:
            log.error("Could not load data from smash.gg")
            raise Exception("Could not load data from smash.gg")

    # -------------------------------------------------------------------------
    if outform == "dict":
        return {
                "tournament": tournament,
                "players": top_players,
                }

    # -------------------------------------------------------------------------
    if outform == "lkrz":
        return "\n".join(
                [ tournament.conf() ] \
                        + list(map(
                            lambda p:p.conf(),
                            top_players,
                            ))
                        )

# =============================================================================
def generate_pic(
        infos_or_lkrzfile = None,
        template = None,
        outform = "svg",
        options = {},
        dir_templates = DEFAULT_DIR_TEMPLATES,
        dir_res = None,
        dir_cache = None,
        log = LOG_DUMMY,
        ):

    if outform not in ["svg", "png"]:
        raise Exception("Unsupported outform")

    if type(infos_or_lkrzfile) == str:
        # TODO : load lkrz as dict infos
        raise NotImplementedError()
    else:
        infos = infos_or_lkrzfile

    # -------------------------------------------------------------------------
    # Build the context which will be passed to the template
    context = {
            "tournament": infos["tournament"].clean_name(
                options.get(
                    "name_seo_delimiter",
                    None
                    )
                ),
            "players" : sorted(
                infos["players"],
                key = lambda p: p.placement,
                ),
            "dir_res_ssbu": dir_res,
            "dir_template": str(dir_templates/template),
            "options": options.get("template_options", []),
            }

    pic = export.generate_pic(
            dir_templates,
            template,
            context,
            outform,
            log = log,
            cachedir = dir_cache,
            options = { "svg_embed_png": options.get("svg_embed_png",False) },
            )

    if pic is None:
        raise Exception("Failed to generate pic")

    return pic

# =============================================================================
def main():

    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            )

    subparsers = parser.add_subparsers(
            dest = "command",
            help = "commands",
            )

    parser.add_argument(
            "--proxy", "-p",
            default = None,
            help = "the proxy to use",
            )

    # -------------------------------------------------------------------------
    init_parser = subparsers.add_parser(
            "init",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            )

    init_parser.add_argument(
            "game",
            default = "ssbu",
            help = "The game you want to initialize the resources for",
            )

    init_parser.add_argument(
            "--imgdir", "-ID",
            type = pathlib.Path,
            default = pathlib.Path(APPDIRS.user_data_dir) / "res",
            help = "The directory we should download the resources to",
            )

    # -------------------------------------------------------------------------
    top8_parser = subparsers.add_parser(
            "top8",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            )

    top8_parser.add_argument(
            "tournament",
            default = None,
            help = "The tournament slug or id",
            )

    top8_parser.add_argument(
            "--token", "-t",
            default = None,
            help = "the authentication token to use",
            )

    top8_parser.add_argument(
            "--imgdir", "-ID",
            type = pathlib.Path,
            default = pathlib.Path(APPDIRS.user_data_dir) / "res",
            help = "The directories containing images, be careful whether " \
                   "you specify an absolute path or a relative one.",
            )
    top8_parser.add_argument(
            "--playerskinsdb", "-PD",
            type = (lambda s: s if s.startswith("http") else pathlib.Path(s)),
            default = ROOTDIR / "data" / "playerskinsdb.json",
            help = "A JSON file path or url matching player tags, characters,"\
                   " sponsors, and preferred skins",
            )
    top8_parser.add_argument(
            "--cachedir", "-CD",
            type = pathlib.Path,
            default = pathlib.Path(APPDIRS.user_cache_dir),
            help = "A directory to use for temporary files",
            )
    top8_parser.add_argument(
            "--templatesdir", "-TD",
            type = pathlib.Path,
            default = DEFAULT_DIR_TEMPLATES,
            help = "The local result templates directory",
            )

    top8_parser.add_argument(
            "--template", "-T",
            default = "rebootlyon2020",
            help = "The local result template to use",
            )
    top8_parser.add_argument(
            "--template-options", "-O",
            action = "append",
            default = [],
            help = "Template-specific options",
            )
    top8_parser.add_argument(
            "--export-options", "-E",
            action = "append",
            default = [],
            help = "Export options (like svg_embed_png)",
            )

    top8_parser.add_argument(
            "--lkrz-file", "-f",
            type = pathlib.Path,
            default = None,
            help = "The lkrz file in which the results are stored ; if it " \
                   "does not exist, one will be created from the smashgg data",
            )
    top8_parser.add_argument(
            "--outfile", "-o",
            type = pathlib.Path,
            default = None,
            help = "The SVG or PNG local result file to output to ; if it's " \
                   "not specified, it will use the tournament slug as name",
            )

    top8_parser.add_argument(
            "--name-seo-delimiter",
            default = None,
            help = "A character that will delimit in a tournament name what " \
                   "really is its name, and what's actually here for SEO "    \
                   "purposes (example: in 'Cornismash #42 - Ultimate Weekly " \
                   "Lyon', only the 'Cornismash #42' is the tournament name, "\
                   "the rest is here to help find the tournament).",
            )
    top8_parser.add_argument(
            "--use-smashgg-prefixes", "-P",
            action = "store_true",
            help = "Use the prefixes (sponsor, team, etc) set by players on " \
                   "smash.gg for the tournament",
                   )

    # -------------------------------------------------------------------------
    parser.add_argument( "--verbose", "-v",
                         default = 0,
                         action = "count",
                         help = "increase verbosity" )

    parser.add_argument( "--version", "-V",
                         default = False,
                         action = "store_true",
                         help = "show version number" )

    # -------------------------------------------------------------------------
    args = parser.parse_args()

    # Set log level
    # -------------------------------------------------------------------------
    log = logging.getLogger(version.NAME)
    log.setLevel(logging.DEBUG)

    log_handler_console = logging.StreamHandler()
    log_handler_console.setLevel(logging.WARNING)

    if(args.verbose >= 2):
        log_handler_console.setLevel(logging.DEBUG)
    elif(args.verbose >=1):
        log_handler_console.setLevel(logging.INFO)
    else:
        log_handler_console.setLevel(logging.WARNING)

    log_formatter_console = logging.Formatter("%(name)s:%(levelname)s: %(message)s")

    log_handler_console.setFormatter(log_formatter_console)

    log.addHandler(log_handler_console)

    # Print version if required
    # -------------------------------------------------------------------------
    if args.version:
        print(version.VERSION_NAME)
        return 0

    # -------------------------------------------------------------------------
    if args.command not in [ "init", "top8" ]:
        parser.print_help()
        return 1

    # -------------------------------------------------------------------------
    if args.command == "init":
        args.imgdir.mkdir(parents=True, exist_ok=True)
        resources.download_res_ssbu(
                dstdir = args.imgdir,
                proxy = args.proxy,
                log = log,
                )
        return 0
    # -------------------------------------------------------------------------
    if args.command == "top8":

        # Initialize PLAYERSKINS db
        log.debug("loading playerskins db from '{}'" \
                .format(args.playerskinsdb))
        try:
            PLAYERSKINS =  requests.get(args.playerskinsdb).json()
            smashgg.GET_PLAYERDATA = (lambda tag: PLAYERSKINS[tag.lower()])
        except:
            with args.playerskinsdb.open("r", encoding="utf8") as f:
                PLAYERSKINS = json.load(f)
                smashgg.GET_PLAYERDATA = (lambda tag: PLAYERSKINS[tag.lower()])

        #
        tournament = None
        top_players = {}

        if args.lkrz_file is not None and args.lkrz_file.exists():
            lkrz = configparser.ConfigParser()
            lkrz.read(str(args.lkrz_file))

            log.info("Loading data from '{}'".format(args.lkrz_file))

            for s in lkrz:
                section = lkrz[s]
                if s == "Tournament":
                    tournament = smashgg.Tournament(
                            id = 0,
                            name = section["name"],
                            slug = section["slug"],
                            startAt = datetime.datetime.strptime(
                                section["date"],
                                "%Y-%m-%d %H:%M:%S",
                                ),
                            numEntrants = int(section["numEntrants"]),
                            venueName = section["location"],
                            )

                elif s.startswith("player "):
                    chars = {}
                    for char in section["characters"].split(","):
                        c = char.strip()
                        charname = c.split("_")[0]
                        charskin = c.split("_")[1].split(" ")[0]
                        charscore = float(c.split("(")[1].split(")")[0])

                        chars[(charname,charskin)] = charscore

                    player = smashgg.Player(
                            id = 0,
                            prefix = section["team"],
                            gamerTag = section["tag"],
                            placement = section["placement"],
                            seeding = section["seeding"],
                            twitterHandle = section["twitter"],
                            chars = chars,
                            )

                    top_players[player.gamerTag] = player

            # Re-sort top players by their placement
            top_players = sorted(
                    top_players.values(),
                    key = lambda p: p.placement,
                    )

        else:

            # Get infos from smash.gg and write the config file
            tournament, top_players = getTournamentTop(
                    id_or_slug = args.tournament,
                    get_prefixes = args.use_smashgg_prefixes,
                    top = 8,
                    token = args.token,
                    proxy = args.proxy,
                    log = log,
                    )

            if tournament is None or top_players is None:
                log.error("Could not load data from smash.gg")
                return 1

            lkrz_data = "\n".join(
                    [ tournament.conf() ] \
                    + list(map(
                        lambda p:p.conf(),
                        top_players,
                        ))
                    )

            if args.lkrz_file is None:
                args.lkrz_file = pathlib.Path(
                        "{}.lkrz".format(tournament.slug)
                        )

            with args.lkrz_file.open("w", encoding="utf8") as f:
                f.write(lkrz_data)

        # Default outfile is 'tournament-slug.svg'
        if args.outfile is None:
            args.outfile = pathlib.Path(
                    "{}.svg".format(tournament.slug),
                    )

        # Build the context which will be passed to the template
        try:
            dir_res_ssbu = args.imgdir.as_uri() # not absolute => error
        except ValueError:
            dir_res_ssbu = args.imgdir.as_posix()

        context = {
                "tournament": tournament.clean_name(args.name_seo_delimiter),
                "players" : sorted(
                    top_players,
                    key = lambda p: p.placement,
                    ),
                "dir_res_ssbu": dir_res_ssbu,
                "dir_template": str(args.templatesdir / args.template),
                "options": args.template_options,
                }

        rv = export.generate_outfile(
                args.templatesdir,
                args.template,
                context,
                args.outfile,
                log = log,
                cachedir = args.cachedir,
                options={"svg_embed_png": "svg_embed_png" in args.export_options},
                )

        if rv is None:
            return 1

        log.info("Successfully saved outfile as '{}'".format(rv))

        return 0

# -----------------------------------------------------------------------------
def getTournamentTop(
        id_or_slug,
        get_prefixes = True,
        top = 8,
        token = "",
        proxy = None,
        log=LOG_DUMMY):
    """Returns a tuple : the smashgg.Tournament object and a list of the top
    smashgg.Player in that tournament."""

    # TODO if url matches challonge
    #
    #data = challonge.get_participants(
    #        api_key = token,
    #        tournament = id_or_slug,
    #        )
    #
    #top_array = []*top
    #for p in data:
    #   top_array[p["participant"]["final_rank"]] = ...

    # -------------------------------------------------------------------------
    # Select the right event (the one with the most entrants or the most sets)
    def selectBiggestEvent(data, log=LOG_DUMMY):

        try:
            event = data["events"][0]
        except:
            log.error("No event found in data")
            log.debug(data)
            return None

        try:
            numEntrants = event["numEntrants"]
        except KeyError:
            numEntrants = event["standings"]["pageInfo"]["total"]

        for e in data["events"]:
            try:
                ne = e["numEntrants"]
            except KeyError:
                ne = e["standings"]["pageInfo"]["total"]

            if ne > numEntrants:
                event = e
                numEntrants = ne

        log.info("Selected Event '{}' with {} entrants" \
                .format(
                    event["name"],
                    numEntrants,
                    ))

        return event

    # -------------------------------------------------------------------------
    data = None

    try:
        data = smashgg.run_query(
                query_name = "getTournamentTopById",
                variables = {
                    "id" : int(id_or_slug), # If this fails, it's a slug
                    "top": top,
                    },
                query_dir = ROOTDIR / "queries",
                token = token,
                proxy = proxy,
                log = log,
                )

    except ValueError:
        data = smashgg.run_query(
                query_name = "getTournamentTopBySlug",
                variables = {
                    "slug" : id_or_slug,
                    "top": top,
                    },
                query_dir = ROOTDIR / "queries",
                token = token,
                proxy = proxy,
                log = log,
                )

    try:
        tournament_data = data["tournament"]
    except:
        log.error("Failed to load Tournaments")
        return None,None

    if tournament_data is None:
        log.error("Failed to load Tournament")
        return None,None

    event = selectBiggestEvent(tournament_data, log)

    if event is None :
        return None,None

    # Get the tournament
    tournament = smashgg.Tournament(
            id = tournament_data["id"],
            slug = tournament_data["slug"],
            name = tournament_data["name"],
            startAt = \
                    datetime.datetime. \
                    fromtimestamp(tournament_data["startAt"]),
            numEntrants = event["standings"]["pageInfo"]["total"],
            venueAddress = tournament_data["venueAddress"],
            venueName = tournament_data["venueName"],
            city = tournament_data["city"],
            countryCode = tournament_data["countryCode"],
            hashtag = tournament_data["hashtag"],
            )


    # Get the top players
    top_players = {}

    standings = event["standings"]["nodes"]

    for standing in standings :

        seeding = None
        for seed in standing["entrant"]["seeds"]:
            # Take the seeding from the phase with *all* Event entrants
            if seed["phase"]["numSeeds"] == tournament.numEntrants:
                seeding = seed["groupSeedNum"]

        participant_data = standing["entrant"]["participants"][0]

        try:
            twitterHandle = participant_data \
                    ["player"] \
                    ["user"] \
                    ["authorizations"] \
                    [0] \
                    ["externalUsername"]
        except TypeError:
            twitterHandle = None

        if get_prefixes:
            prefix = participant_data["prefix"]
        else:
            prefix = ""

        player = smashgg.Player(
                id = standing["entrant"]["id"],
                prefix = prefix,
                gamerTag = participant_data["gamerTag"],
                placement = standing["placement"],
                seeding = seeding,
                twitterHandle = twitterHandle,
                )

        top_players[player.id] = player

    # -------------------------------------------------------------------------
    # Now, we need to find which characters those top players chose
    data = None

    data = smashgg.run_query(
            query_name = "getCharsByTournamentIdAndEntrantIds",
            variables = {
                "tournamentId" : int(tournament.id),
                "entrantIds": [ id for id in top_players.keys() ],
                },
            query_dir = ROOTDIR / "queries",
            token = token,
            proxy = proxy,
            log = log,
            )

    try:
        tournament_data = data["tournament"]
    except:
        log.error("Failed to load Tournament")
        return None,None

    if tournament_data is None:
        log.error("Failed to load Tournament")
        return None,None

    event = selectBiggestEvent(tournament_data, log)

    if event is None :
        return None,None

    # TODO check that sets number is < to hardcoded 100 max value (cf query)
    sets = event["sets"]["nodes"]

    for s in sets:
        try:
            for g in s["games"]:

                winnerId = g["winnerId"]

                for slct in g["selections"]:

                    if slct["selectionType"] == "CHARACTER":
                        eid = slct["entrant"]["id"]
                        try:
                            top_players[eid].add_character_selection(
                                    character = slct["selectionValue"],
                                    win = (winnerId == eid),
                                    )
                        except KeyError:
                            pass
        except TypeError:
            # If some games or selections are null, this can happen
            continue

    # Sort top_players by rank instead of id:
    top_players_sorted = sorted(
                top_players.values(),
                key = lambda p: p.placement,
                )

    # Return the data
    return tournament, top_players_sorted

# =============================================================================
if __name__ == '__main__':
    rv = main()
    sys.exit(rv)

