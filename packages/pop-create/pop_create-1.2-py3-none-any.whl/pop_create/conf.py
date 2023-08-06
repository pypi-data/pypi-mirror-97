import os

CLI_CONFIG = {
    "project_name": {"subcommands": ["_global_"], "options": ["-n", "--name"],},
    "dyne": {"subcommands": ["_global_"], "options": ["-d"]},
    "ignore_empty_warning": {
        "subcommands": ["_global_"],
        "options": ["-i"],
        "action": "store_true",
    },
    "directory": {"options": ["-D"], "subcommands": ["_global_"]},
    "vertical": {
        "subcommands": ["_global_"],
        "action": "store_true",
        "options": ["-tv"],
    },
}
CONFIG = {
    "project_name": {
        "help": "The name of the project that is being created",
        "default": None,
    },
    "vertical": {
        "default": False,
        "help": "Build a vertically app-merged project, it's entrypoint is in another project",
    },
    "ignore_empty_warning": {
        "default": False,
        "help": "Allow the script to run in a non-empty directory, potentially overwriting files",
    },
    "dyne": {
        "default": [],
        "nargs": "*",
        "help": "A space delimited list of additional dynamic names for vertical app-merging",
    },
    "directory": {
        "default": os.getcwd(),
        "help": "The directory to create the project in",
    },
}

SUBCOMMANDS = {
    "seed": {"help": "Seed a traditional pop project"},
    "tests": {"help": "Create the tests for a traditional pop-project"},
    "docs": {"help": "Create the sphynx tooling for this project"},
    "cicd": {"help": "Create the cicd tooling for this project"},
}
DYNE = {
    "pop_create": ["pop_create"],
}
