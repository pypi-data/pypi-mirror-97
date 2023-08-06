import io
import pathlib
import sys
import zipfile

import requests

from .characters_ssbu import EVERYONE

# -----------------------------------------------------------------------------
def download_file(url, with_progressbar = True, proxy = None):

    r = requests.get(
            url,
            stream = with_progressbar,
            proxies = { "https": proxy, "http": proxy },
            )

    if not with_progressbar:
        return io.BytesIO(r.content)

    total = r.headers.get("content-length")

    f = io.BytesIO()

    if total is not None:
        downloaded = 0
        total = int(total)
        for data in r.iter_content(
                chunk_size = max(int(total/1000), 1024*1024),
                ):
            f.write(data)
            downloaded += len(data)
            done = int(50*downloaded/total)
            sys.stdout.write( "\r[{}{}] ({:02d}%)".format(
                "█" * done,
                " " * (50-done),
                done*2,
                ) )
            sys.stdout.flush()
        sys.stdout.write("\n")
    else:
        f = write(r.content)

    return f

# -----------------------------------------------------------------------------
def download_res_ssbu(dstdir, proxy = None, log=None):
    """Downloads SSBU resources from spriters and rename them according to
    lokrez expectations"""

    stock_icons_url = "https://www.spriters-resource.com/download/111395/"

    # -------------------------------------------------------------------------
    # Download stock icons
    log.warning("Downloading stock icons...")
    fstocks = download_file(stock_icons_url, proxy = proxy)
    zfstocks = zipfile.ZipFile(fstocks)

    # Iter over each character
    for character in EVERYONE:
        log.warning("Downloading images for {}...".format(character.name))

        # Create directory for this character
        chardir = dstdir / character.name

        try:
            chardir.mkdir()

        except FileExistsError:
            log.info(
                    "Directory already exists for {}".format(character.name)
                    )
                
            try:
                next(chardir.iterdir())
                log.warning(
                        "Directory not empty for {}, skipping" \
                                .format(character.name)
                        )
                continue
            except StopIteration:
                log.info(
                        "Directory empty, downloading",
                        )

        # Download urls & write image files
        for url in character.spritersurls:
            try:
                f = download_file(url, proxy = proxy)
            except Exception as e:
                try:
                    log.warning("Download failed ({}), retrying".format(e))
                    f = download_file(url, proxy = proxy)
                except Exception as e:
                    log.error("Download failed({})".format(e))
                    log.debug(e, exc_info = True)
                    continue

            with zipfile.ZipFile(f) as zfchar:
                for zf in [zfchar,zfstocks]:
                    for source_filename in zf.namelist():

                        if "No Gamma Fix" in source_filename:
                            continue

                        if character.codename not in source_filename:
                            continue

                        target_filename = pathlib.Path(source_filename).name

                        if target_filename in ["","Tag.txt"]:
                            continue

                        target_filename = pathlib.Path(source_filename).name

                        target_filename = target_filename.replace(
                                character.codename,
                                character.name,
                                )

                        log.debug("Writing file '{}'".format(target_filename))

                        target_filename = chardir / target_filename

                        with open(str(target_filename), "wb") as tf:
                            tf.write(zf.read(source_filename))

# =============================================================================
if __name__ == '__main__':

    import argparse
    import logging
    import tempfile

    logging.basicConfig(
            level = logging.DEBUG,
            format = "%(message)s",
            )

    parser = argparse.ArgumentParser()

    parser.add_argument(
            "dstdir",
            default = None,
            help = "directory where to store the downloaded resources " \
                   "(default to a temporary file)",
                   )

    args = parser.parse_args()

    if args.dstdir is None:
        args.dstdir = tempfile.mkdtemp()
        logging.warning(
                "Storing in temporary directory : {}".format(args.dstdir)
                )

    download_res_ssbu(
            dstdir = args.dstdir,
            log = logging,
            )
