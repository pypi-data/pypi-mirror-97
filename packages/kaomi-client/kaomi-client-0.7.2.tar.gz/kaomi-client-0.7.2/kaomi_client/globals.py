from . import __version__

PERMS_MASK = 0o777

SERVER_PORT_DEFAULT = 47000

API_PATHS = {
    "upload_file":            "api/v1/files/upload",
    "create_directory":       "api/v1/files/mkdir",
    "delete_filesystem_node": "api/v1/files/delete_node",
    "execute_action":         "api/v1/actions/execute",
    "delete_by_regex":        "api/v1/files/delete_by_regex"
}

EXIT_STATUS_RESOLVER = {
    0: "0 = Success",
    1: "1 = Client Error",
    2: "2 = Server Error: comunication",
    3: "3 = Server Error: permissions",
    4: "4 = Server Error: application"
}

# la versione dell'agent viene presa dall'init
AGENT_VERSION = __version__
