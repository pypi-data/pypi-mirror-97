NAME = "lokrez"
DESCRIPTION = "Smash.gg-connected top8 graphics generator for Super Smash " \
              "Bros Ultimate tournaments"

URL = "https://git.lertsenem.com/lertsenem/ssbu_lokrez"
AUTHOR = "Lertsenem"
ENTITY = "Smash@Lyon"
AUTHOR_EMAIL = "lertsenem@lertsenem.com"
ENTITY_EMAIL = "dev@smashatlyon.com"

VERSION_MAJOR = 3
VERSION_MINOR = 3
VERSION_PATCH = 1

__version__ = "{}.{}.{}".format(
        VERSION_MAJOR,
        VERSION_MINOR,
        VERSION_PATCH,
        )

VERSION_NAME = "{} - {}".format(
        NAME,
        __version__,
        )

__license__ = "MIT"
