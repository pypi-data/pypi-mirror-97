CLI_CONFIG = {
    "simple_cloud_name": {
        "options": ["--cloud", "--cloud-name"],
        "subcommands": ["idem-cloud"],
        "dyne": "pop_create",
    },
    "openapi_spec": {
        "options": ["--spec"],
        "subcommands": ["exec.openapi3"],
        "dyne": "pop_create",
    },
}
CONFIG = {
    "simple_cloud_name": {
        "default": None,
        "help": "Short name of the cloud being bootstrapped",
    },
    "openapi_spec": {
        "default": None,
        "help": "The url or file path to an openApi3 spec",
    },
}
SUBCOMMANDS = {
    "idem-cloud": {"help": "Boostrap an idem cloud project", "dyne": "pop_create"},
    "exec.openapi3": {
        "help": "Create exec modules based off of openapi3",
        "dyne": "pop_create",
    },
}
DYNE = {"pop_create": ["pop_create"]}
