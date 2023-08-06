# -------------------------------------------------------------------------
class SSBUCharacter:
    """Infos needed about an SSBU character"""
    def __init__(
            self,
            name,
            codename,
            spritersurls,
            smashggid = None,
            ):
        self.spritersurls = spritersurls
        self.smashggid = smashggid
        self.name = name
        self.codename = codename
        
# -------------------------------------------------------------------------
EVERYONE = [
        SSBUCharacter(
            smashggid = 1530,
            name = "banjo & kazooie",
            codename = "buddy",
            spritersurls = [
                "https://www.spriters-resource.com/download/121027/",
                ],
            ),
        SSBUCharacter(
            smashggid = None,
            name = "bayonetta",
            codename = "bayonetta",
            spritersurls = [
                "https://www.spriters-resource.com/download/111299/",
                ],
            ),
        SSBUCharacter(
            smashggid = 1272,
            name = "bowser jr",
            codename = "koopajr",
            spritersurls = [
                "https://www.spriters-resource.com/download/111303/",
                ],
            ),
        SSBUCharacter(
            smashggid = 1273,
            name = "bowser",
            codename = "koopa",
            spritersurls = [
                "https://www.spriters-resource.com/download/111302/",
                ],
            ),
        SSBUCharacter(
            smashggid = 1539,
            name = "byleth",
            codename = "master",
            spritersurls = [
                "https://www.spriters-resource.com/download/125348/",
                ],
            ),
        SSBUCharacter(
            smashggid = 1274,
            name = "captain falcon",
            codename = "captain",
            spritersurls = [
                "https://www.spriters-resource.com/download/111304/"
                ],
            ),
        SSBUCharacter(
                smashggid = None,
                name = "charizard",
                codename = "plizardon",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111351/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1409,
                name = "chrom",
                codename = "chrom",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111305/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1275,
                name = "cloud",
                codename = "cloud",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111306/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "corrin",
                codename = "kamui",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111307/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1277,
                name = "daisy",
                codename = "daisy",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111308/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "dark pit",
                codename = "pitb",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111309/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1279,
                name = "diddy kong",
                codename = "diddy",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111311/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1280,
                name = "donkey kong",
                codename = "donkey",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111312/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1282,
                name = "dr mario",
                codename = "mariod",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111313/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1283,
                name = "duck hunt",
                codename = "duckhunt",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111314/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1285,
                name = "falco",
                codename = "falco",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111315/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1286,
                name = "fox",
                codename = "fox",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111316/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1287,
                name = "ganondorf",
                codename = "ganon",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111317/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "greninja",
                codename = "gekkouga",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111318/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1526,
                name = "hero",
                codename = "brave",
                spritersurls = [
                    "https://www.spriters-resource.com/download/119842/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1290,
                name = "ice climbers",
                codename = "ice_climber",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111319/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1291,
                name = "ike",
                codename = "ike",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111320/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1292,
                name = "inkling",
                codename = "inkling",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111322/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "ivysaur",
                codename = "pfushigisou",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111352/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1293,
                name = "jigglypuff",
                codename = "purin",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111324/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1410,
                name = "ken",
                codename = "ken",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111325/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1294,
                name = "king dedede",
                codename = "dedede",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111326/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1295,
                name = "kirby",
                codename = "kirby",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111328/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1296,
                name = "link",
                codename = "link",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111329/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1297,
                name = "little mac",
                codename = "littlemac",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111330/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1298,
                name = "lucario",
                codename = "lucario",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111331/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1299,
                name = "lucas",
                codename = "lucas",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111332/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1300,
                name = "lucina",
                codename = "lucina",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111333/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1301,
                name = "luigi",
                codename = "luigi",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111334/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1302,
                name = "mario",
                codename = "mario",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111335/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "marth",
                codename = "marth",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111336/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1305,
                name = "mega man",
                codename = "rockman",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111337/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1307,
                name = "meta knight",
                codename = "metaknight",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111338/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1310,
                name = "mewtwo",
                codename = "mewtwo",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111339/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "mii fighter",
                codename = "miifighter",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111340/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1415,
                name = "mii gunner",
                codename = "miigunner",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111340/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "mii swordsman",
                codename = "miiswordsman",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111340/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1313,
                name = "ness",
                codename = "ness",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111342/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1314,
                name = "olimar",
                codename = "pikmin",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111343/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1315,
                name = "pacman",
                codename = "pacman",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111344/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1316,
                name = "palutena",
                codename = "palutena",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111345/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1317,
                name = "peach",
                codename = "peach",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111346/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1318,
                name = "pichu",
                codename = "pichu",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111347/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1319,
                name = "pikachu",
                codename = "pikachu",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111348/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1320,
                name = "pit",
                codename = "pit",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111349/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1321,
                name = "pokemon trainer",
                codename = "ptrainer",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111350/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1412,
                name = "richter",
                codename = "richter",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111354/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1322,
                name = "ridley",
                codename = "ridley",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111355/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1323,
                name = "rob",
                codename = "robot",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111356/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1324,
                name = "robin",
                codename = "reflet",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111357/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1325,
                name = "rosalina and luma",
                codename = "rosetta",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111358/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1326,
                name = "roy",
                codename = "roy",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111359/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1327,
                name = "ryu",
                codename = "ryu",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111360/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1328,
                name = "samus",
                codename = "samus",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111361/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1329,
                name = "sheik",
                codename = "sheik",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111362/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1330,
                name = "shulk",
                codename = "shulk",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111363/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "simon",
                codename = "simon",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111364/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1331,
                name = "snake",
                codename = "snake",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111365/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1332,
                name = "sonic",
                codename = "sonic",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111366/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "squirtle",
                codename = "pzenigame",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111353/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1333,
                name = "toon link",
                codename = "toonlink",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111367/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1334,
                name = "villager",
                codename = "murabito",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111368/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1335,
                name = "wario",
                codename = "wario",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111369/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1336,
                name = "wii fit trainer",
                codename = "wiifit",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111370/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1337,
                name = "wolf",
                codename = "wolf",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111371/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1338,
                name = "yoshi",
                codename = "yoshi",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111372/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1339,
                name = "young link",
                codename = "younglink",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111373/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1340,
                name = "zelda",
                codename = "zelda",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111374/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1341,
                name = "zero suit samus",
                codename = "szerosuit",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111375/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1405,
                name = "mr game and watch",
                codename = "gamewatch",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111341/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1406,
                name = "incineroar",
                codename = "gaogaen",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111321/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1407,
                name = "king k rool",
                codename = "krool",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111327/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1408,
                name = "dark samus",
                codename = "samusd",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111310/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1413,
                name = "isabelle",
                codename = "shizue",
                spritersurls = [
                    "https://www.spriters-resource.com/download/111323/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1441,
                name = "piranha plant",
                codename = "packun",
                spritersurls = [
                    "https://www.spriters-resource.com/download/113440/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1453,
                name = "joker",
                codename = "jack",
                spritersurls = [
                    "https://www.spriters-resource.com/download/116168/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1532,
                name = "terry",
                codename = "dolly",
                spritersurls = [
                    "https://www.spriters-resource.com/download/123089/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1747,
                name = "min min",
                codename = "tantan",
                spritersurls = [
                    "https://www.spriters-resource.com/download/134242/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1766,
                name = "steve",
                codename = "pickel",
                spritersurls = [
                    "https://www.spriters-resource.com/download/140939/",
                    ],
                ),
        SSBUCharacter(
                smashggid = 1777,
                name = "sephiroth",
                codename = "edge",
                spritersurls = [
                    "https://www.spriters-resource.com/download/145102/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "pyra",
                codename = "eflame_only",
                spritersurls = [
                    "https://www.spriters-resource.com/download/149626/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "pyra & mythra",
                codename = "eflame_first",
                spritersurls = [
                    "https://www.spriters-resource.com/download/149627/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "mythra",
                codename = "elight_only",
                spritersurls = [
                    "https://www.spriters-resource.com/download/149628/",
                    ],
                ),
        SSBUCharacter(
                smashggid = None,
                name = "mythra & pyra",
                codename = "elight_first",
                spritersurls = [
                    "https://www.spriters-resource.com/download/149629/",
                    ],
                ),
        ]

