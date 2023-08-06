import distutils, distutils.util
import os
import setuptools
import sys

import lokrez, lokrez.version

# Load README for long_description
with open("README.adoc", "r") as fh:
    long_description = fh.read()

# Windows build
if os.name == "nt":
    import cx_Freeze

    arch = distutils.util.get_platform().split("-")[-1]

    build_exe_options = {
            "packages": ["os"],
            "include_msvcr": True,
            "include_files": [ "lokrez/data", "lokrez/templates", "lokrez/queries" ],
            "includes": ["idna.idnadata"], # Because of cx-freeze bug
            }

    bdist_msi_options = {
            "upgrade_code": "{123456789-1337-8483-ABCD-DEADBEEFCAFE}",
            "add_to_path": True,
            "initial_target_dir": r"[LocalAppDataFolder]\{}\{}" \
                    .format(
                        lokrez.version.ENTITY,
                        lokrez.version.NAME,
                        ),
            }

    base = None

    cx_Freeze.setup(
            name = lokrez.version.NAME,
            version = lokrez.version.__version__.replace("dev", "1337"),
            author = lokrez.version.AUTHOR,
            author_email = lokrez.version.AUTHOR_EMAIL,
            description = lokrez.version.DESCRIPTION,
            install_requires = [
                "jinja2",
                "requests",
                "appdirs",
                ],
            options = {
                "build_exe": build_exe_options,
                "bdist_msi": bdist_msi_options,
                },

            executables = [
                    cx_Freeze.Executable(
                        script = "lokrez/__main__.py",
                        targetName = "{}.exe".format(lokrez.version.NAME),
                        base = base,
                        ),
                    ],
            )

    sys.exit(0)

# Linux build
if os.name == "posix":

    setuptools.setup(
            name = lokrez.version.NAME,
            version = lokrez.__version__,
            author = lokrez.version.AUTHOR,
            author_email = lokrez.version.AUTHOR_EMAIL,
            description = lokrez.version.DESCRIPTION,
            long_description = long_description,
            long_description_content_type = "text/plain",
            url = lokrez.version.URL,
            packages = ["lokrez"],
            install_requires = [
                "jinja2",
                "requests",
                "appdirs",
                ],
            license = lokrez.version.__license__,
            classifiers = [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Intended Audience :: End Users/Desktop",
                "Topic :: Multimedia :: Graphics",
                "Environment :: Console"
                ],
            python_requires = ">=3.5",
            keywords = "smash ultimate local results esport smashgg",
#        data_files = ("res", ["res/playerskinsdb.json"])
            package_data = {
                "lokrez": [
                    "data/*.json",
                    "queries/*.gql",
                    "templates/*/*.j2",
                    "templates/*/*/*.j2",
                    ],
                },
            entry_points = {
                "console_scripts": [
                    "lokrez = lokrez:main",
                    ],
                },
            )
